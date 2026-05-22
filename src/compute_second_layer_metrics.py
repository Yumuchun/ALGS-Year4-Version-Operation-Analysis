#!/usr/bin/env python3
"""Compute second-layer portfolio metrics from scraped ALGS Year 4 data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "portfolio_algs_year4"
OUT_DIR = ROOT / "portfolio" / "analysis_outputs"

EVENT_ORDER = [
    "playoffs_split1",
    "midseason_ewc_split1",
    "playoffs_split2",
    "championship_split2",
]

LEGEND_CLASS = {
    "Ash": "Assault",
    "Ballistic": "Assault",
    "Bangalore": "Assault",
    "Fuse": "Assault",
    "Mad Maggie": "Assault",
    "Alter": "Skirmisher",
    "Horizon": "Skirmisher",
    "Octane": "Skirmisher",
    "Pathfinder": "Skirmisher",
    "Revenant": "Skirmisher",
    "Valkyrie": "Skirmisher",
    "Wraith": "Skirmisher",
    "Bloodhound": "Recon",
    "Crypto": "Recon",
    "Seer": "Recon",
    "Vantage": "Recon",
    "Catalyst": "Controller",
    "Caustic": "Controller",
    "Rampart": "Controller",
    "Wattson": "Controller",
    "Conduit": "Support",
    "Gibraltar": "Support",
    "Lifeline": "Support",
    "Loba": "Support",
    "Mirage": "Support",
    "Newcastle": "Support",
}

WEAPON_CATEGORY = {
    "30-30 Repeater": "Precision",
    "Bocek Compound Bow": "Precision",
    "Charge Rifle": "Precision",
    "G7 Scout": "Precision",
    "Kraber .50-Cal Sniper": "Precision",
    "Longbow DMR": "Precision",
    "Sentinel": "Precision",
    "Triple Take": "Precision",
    "Wingman": "Precision",
    "HAVOC Rifle": "AR",
    "Hemlok": "AR",
    "Nemesis Burst AR": "AR",
    "R-301 Carbine": "AR",
    "VK-47 Flatline": "AR",
    "Alternator SMG": "SMG",
    "C.A.R.": "SMG",
    "Prowler Burst PDW": "SMG",
    "R-99 SMG": "SMG",
    "Volt SMG": "SMG",
    "RE-45": "Pistol/SMG",
    "Devotion LMG": "LMG",
    "L-STAR EMG": "LMG",
    "M600 Spitfire": "LMG",
    "Rampage LMG": "LMG",
    "EVA-8 Auto": "Shotgun",
    "Mastiff Shotgun": "Shotgun",
    "Mozambique Shotgun": "Shotgun",
    "Peacekeeper": "Shotgun",
    "Mozambique (Akimbo)": "Shotgun/Akimbo",
    "P2020": "Pistol/Akimbo",
    "Arc Star": "Ordnance",
    "Frag Grenade": "Ordnance",
    "Thermite Grenade": "Ordnance",
    "Fall": "Other",
    "Melee": "Other",
}


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False),
        errors="coerce",
    )


def ordered(df: pd.DataFrame, column: str = "event_slug") -> pd.DataFrame:
    result = df.copy()
    result[column] = pd.Categorical(result[column], categories=EVENT_ORDER, ordered=True)
    return result.sort_values(column)


def write(df: pd.DataFrame, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ordered_df = ordered(df) if "event_slug" in df.columns else df
    ordered_df.to_csv(OUT_DIR / name, index=False)


def score_metrics() -> None:
    scores = pd.read_csv(DATA_DIR / "match_scores.csv")
    for col in ["kills", "total_points", "placement_points_reported", "placement"]:
        scores[col] = pd.to_numeric(scores[col], errors="coerce")

    event = scores.groupby("event_slug").agg(
        games=("game_id", "nunique"),
        team_games=("team", "count"),
        kills=("kills", "sum"),
        placement_pts=("placement_points_reported", "sum"),
        total_pts=("total_points", "sum"),
        avg_kills_team_game=("kills", "mean"),
        avg_total_team_game=("total_points", "mean"),
    )
    event["kill_point_share"] = event["kills"] / event["total_pts"]
    event["kills_per_game"] = event["kills"] / event["games"]
    event["placement_pts_per_game"] = event["placement_pts"] / event["games"]
    write(event.reset_index(), "score_response_by_event.csv")

    scores["low_kill_top5_zone_proxy"] = (scores["placement"] <= 5) & (scores["kills"] <= 1)
    scores["high_kill_low_place_edge_proxy"] = (scores["placement"] > 10) & (scores["kills"] >= 5)
    scores["high_kill_top5_hybrid_proxy"] = (scores["placement"] <= 5) & (scores["kills"] >= 5)
    scores["low_kill_low_place_bad"] = (scores["placement"] > 10) & (scores["kills"] <= 1)

    patterns = scores.groupby("event_slug").agg(
        team_games=("team", "count"),
        low_kill_top5_zone_pct=("low_kill_top5_zone_proxy", "mean"),
        high_kill_low_place_edge_pct=("high_kill_low_place_edge_proxy", "mean"),
        high_kill_top5_hybrid_pct=("high_kill_top5_hybrid_proxy", "mean"),
        low_kill_low_place_bad_pct=("low_kill_low_place_bad", "mean"),
        avg_kills_top5=("kills", lambda s: s[scores.loc[s.index, "placement"] <= 5].mean()),
        avg_kills_outside_top10=("kills", lambda s: s[scores.loc[s.index, "placement"] > 10].mean()),
    )
    for col in [
        "low_kill_top5_zone_pct",
        "high_kill_low_place_edge_pct",
        "high_kill_top5_hybrid_pct",
        "low_kill_low_place_bad_pct",
    ]:
        patterns[col] = patterns[col] * 100
    write(patterns.reset_index(), "combat_pattern_by_event.csv")

    by_map = scores.groupby(["event_slug", "map_name"]).agg(
        games=("game_id", "nunique"),
        kills=("kills", "sum"),
        total_pts=("total_points", "sum"),
        avg_kills_team_game=("kills", "mean"),
        avg_total_team_game=("total_points", "mean"),
        low_kill_top5_zone_pct=("low_kill_top5_zone_proxy", "mean"),
        high_kill_low_place_edge_pct=("high_kill_low_place_edge_proxy", "mean"),
        high_kill_top5_hybrid_pct=("high_kill_top5_hybrid_proxy", "mean"),
    )
    by_map["kill_point_share"] = by_map["kills"] / by_map["total_pts"]
    for col in ["low_kill_top5_zone_pct", "high_kill_low_place_edge_pct", "high_kill_top5_hybrid_pct"]:
        by_map[col] = by_map[col] * 100
    write(by_map.reset_index(), "score_response_by_map.csv")


def reset_signal_metrics() -> None:
    """Measure whether later metas created more reset/second-chance space.

    `match_scores.csv` is the official scoring surface for credited kills.
    `game_team_stats.csv` adds match telemetry such as deaths, revives (`rez`)
    and respawns (`rspn`). Keeping them separate avoids treating every death as
    a scored kill.
    """
    scores = pd.read_csv(DATA_DIR / "match_scores.csv")
    team_stats = pd.read_csv(DATA_DIR / "game_team_stats.csv")

    for col in ["kills", "total_points"]:
        scores[col] = numeric(scores[col])
    for col in ["kills", "deaths", "knocks", "times_knocked", "rez", "rspn", "ring_dmg"]:
        team_stats[col] = numeric(team_stats[col])

    score_games = scores.groupby(["event_slug", "game_id"]).agg(
        score_kills=("kills", "sum"),
        score_total_points=("total_points", "sum"),
    ).reset_index()
    stat_games = team_stats.groupby(["event_slug", "game_id"]).agg(
        stat_kills=("kills", "sum"),
        deaths=("deaths", "sum"),
        knocks=("knocks", "sum"),
        times_knocked=("times_knocked", "sum"),
        revives=("rez", "sum"),
        respawns=("rspn", "sum"),
        ring_damage=("ring_dmg", "sum"),
    ).reset_index()

    games = score_games.merge(stat_games, on=["event_slug", "game_id"], how="left")
    games["br_baseline_kills"] = 57
    games["score_kills_above_baseline"] = games["score_kills"] - games["br_baseline_kills"]
    games["deaths_above_60"] = games["deaths"] - 60
    write(games, "reset_signal_by_game.csv")

    event = games.groupby("event_slug").agg(
        games=("game_id", "nunique"),
        score_kills_per_game=("score_kills", "mean"),
        deaths_per_game=("deaths", "mean"),
        respawns_per_game=("respawns", "mean"),
        revives_per_game=("revives", "mean"),
        knocks_per_game=("knocks", "mean"),
        ring_damage_per_game=("ring_damage", "mean"),
        score_kills_above_baseline=("score_kills_above_baseline", "mean"),
        deaths_above_60=("deaths_above_60", "mean"),
    ).reset_index()
    write(event, "reset_signal_by_event.csv")


def team_style_metrics() -> None:
    teams = pd.read_csv(DATA_DIR / "overview_team_stats.csv")
    for col in [
        "games",
        "kills",
        "place_pts",
        "total_pts",
        "top_5s",
        "top_10s",
        "dmg_dealt",
        "knocks",
        "times_knocked",
        "deaths",
    ]:
        teams[col] = numeric(teams[col])

    teams["kill_share"] = teams["kills"] / teams["total_pts"]
    teams["placement_share"] = teams["place_pts"] / teams["total_pts"]
    teams["kills_per_game"] = teams["kills"] / teams["games"]
    teams["place_pts_per_game"] = teams["place_pts"] / teams["games"]
    teams["total_pts_per_game"] = teams["total_pts"] / teams["games"]
    teams["top5_rate"] = teams["top_5s"] / teams["games"]
    teams["top10_rate"] = teams["top_10s"] / teams["games"]

    style_rows = []
    for event_slug, group in teams.groupby("event_slug"):
        kill_median = group["kill_share"].median()
        top5_median = group["top5_rate"].median()
        for _, row in group.iterrows():
            if row["kill_share"] >= kill_median and row["top5_rate"] >= top5_median:
                style = "hybrid_high_yield"
            elif row["kill_share"] >= kill_median and row["top5_rate"] < top5_median:
                style = "edge_fighting_proxy"
            elif row["kill_share"] < kill_median and row["top5_rate"] >= top5_median:
                style = "zone_control_proxy"
            else:
                style = "low_yield_or_unstable"
            style_rows.append({**row.to_dict(), "style": style})

    style_df = pd.DataFrame(style_rows)
    write(style_df, "team_style_by_event.csv")

    summary = style_df.groupby(["event_slug", "style"]).agg(
        teams=("team", "count"),
        avg_total_ppg=("total_pts_per_game", "mean"),
        avg_kill_share=("kill_share", "mean"),
        avg_top5_rate=("top5_rate", "mean"),
        avg_kills_per_game=("kills_per_game", "mean"),
        avg_place_ppg=("place_pts_per_game", "mean"),
    ).reset_index()
    write(summary, "team_style_summary.csv")


def legend_and_composition_metrics() -> None:
    legends = pd.read_csv(DATA_DIR / "overview_legend_meta.csv")
    for col in [
        "pick_rate_pct",
        "win_rate_pct",
        "top_5_rate_pct",
        "top_7_conversion_rate_pct",
        "fwr_pct",
        "total_occurrences",
        "avg_placement",
    ]:
        legends[col] = numeric(legends[col])
    legends["class"] = legends["legend"].map(LEGEND_CLASS).fillna("Other")
    write(legends, "legend_pick_by_event.csv")

    class_share = legends.groupby(["event_slug", "class"]).agg(
        pick_rate_pct_sum=("pick_rate_pct", "sum"),
        occurrences=("total_occurrences", "sum"),
    ).reset_index()
    write(class_share, "legend_class_share_by_event.csv")

    comps = pd.read_csv(DATA_DIR / "overview_composition_meta.csv")
    for col in ["pick_rate_pct", "win_rate_pct", "top_5_rate_pct", "total_occurrences", "avg_placement", "fwr_pct"]:
        comps[col] = numeric(comps[col])
    write(comps, "composition_meta_by_event.csv")

    concentration_rows = []
    for event_slug, group in comps.groupby("event_slug"):
        group = group.sort_values("pick_rate_pct", ascending=False)
        concentration_rows.append(
            {
                "event_slug": event_slug,
                "composition_count": len(group),
                "top1_composition": group.iloc[0]["composition"],
                "top1_pick_rate_pct": group.iloc[0]["pick_rate_pct"],
                "top3_pick_rate_pct_sum": group.head(3)["pick_rate_pct"].sum(),
                "top5_pick_rate_pct_sum": group.head(5)["pick_rate_pct"].sum(),
            }
        )
    write(pd.DataFrame(concentration_rows), "composition_concentration_by_event.csv")


def weapon_metrics() -> None:
    weapons = pd.read_csv(DATA_DIR / "weapon_stats.csv")
    weapons = weapons[weapons["source_scope"] == "overview"].copy()
    for col in [
        "kills",
        "damage",
        "knockdowns",
        "times_knocked",
        "shots",
        "hits",
        "playtime_seconds",
        "max_kill_range",
        "max_damage_range",
        "fwr_pct",
    ]:
        weapons[col] = pd.to_numeric(weapons[col], errors="coerce")
    weapons["category"] = weapons["weapon"].map(WEAPON_CATEGORY).fillna("Other")

    totals = weapons.groupby("event_slug").agg(total_kills=("kills", "sum"), total_damage=("damage", "sum"))
    weapons = weapons.merge(totals, on="event_slug")
    weapons["kill_share_pct"] = 100 * weapons["kills"] / weapons["total_kills"]
    weapons["damage_share_pct"] = 100 * weapons["damage"] / weapons["total_damage"]
    write(weapons, "weapon_meta_by_event.csv")

    weapon_rows = weapons[~weapons["category"].isin(["Ordnance", "Other"])].copy()
    category = weapon_rows.groupby(["event_slug", "category"]).agg(
        kills=("kills", "sum"),
        damage=("damage", "sum"),
        playtime_seconds=("playtime_seconds", "sum"),
    ).reset_index()
    category_totals = category.groupby("event_slug").agg(total_kills=("kills", "sum"), total_damage=("damage", "sum"))
    category = category.merge(category_totals, on="event_slug")
    category["kill_share_pct"] = 100 * category["kills"] / category["total_kills"]
    category["damage_share_pct"] = 100 * category["damage"] / category["total_damage"]
    write(category, "weapon_category_by_event.csv")


def weighted_mean(df: pd.DataFrame, value_col: str, weight_col: str = "total_occurrences") -> float:
    valid = df[[value_col, weight_col]].dropna()
    if valid.empty or valid[weight_col].sum() == 0:
        return float("nan")
    return float((valid[value_col] * valid[weight_col]).sum() / valid[weight_col].sum())


def style_metric(style_df: pd.DataFrame, style: str, metric: str) -> float:
    row = style_df[style_df["style"] == style]
    if row.empty:
        return float("nan")
    return float(row.iloc[0][metric])


def classify_concentration(top1: float, top3: float, top5: float) -> str:
    if top1 >= 50 and top3 >= 80 and top5 >= 90:
        return "single_dominant"
    if top1 >= 50:
        return "one_core_many_options"
    if top5 >= 80:
        return "multi_core_narrow_pool"
    if top1 < 25 and top3 < 55:
        return "open_or_testing"
    return "moderate_convergence"


def classify_overall_risk(
    concentration_type: str,
    top_legend_pick: float,
    dominant_class_slot: float,
    top_weapon_category_share: float,
    top_weapon_share: float,
    revives_per_game: float,
    respawns_per_game: float,
) -> str:
    score = 0
    score += {
        "single_dominant": 3,
        "one_core_many_options": 2,
        "multi_core_narrow_pool": 2,
        "moderate_convergence": 1,
        "open_or_testing": 0,
    }[concentration_type]
    if top_legend_pick >= 90:
        score += 3
    elif top_legend_pick >= 80:
        score += 2
    elif top_legend_pick >= 65:
        score += 1
    if dominant_class_slot >= 180:
        score += 3
    elif dominant_class_slot >= 150:
        score += 2
    elif dominant_class_slot >= 90:
        score += 1
    if top_weapon_category_share >= 60:
        score += 3
    elif top_weapon_category_share >= 50 or top_weapon_share >= 30:
        score += 2
    elif top_weapon_category_share >= 40 or top_weapon_share >= 25:
        score += 1
    if revives_per_game >= 15:
        score += 2
    elif revives_per_game >= 10 or respawns_per_game >= 3.5:
        score += 1

    if score >= 10:
        return "critical"
    if score >= 7:
        return "high"
    if score >= 4:
        return "medium"
    return "low"


def operational_balance_metrics() -> None:
    """Build fourth-layer operational risk flags from existing analysis tables."""
    concentration = pd.read_csv(OUT_DIR / "composition_concentration_by_event.csv")
    comps = pd.read_csv(OUT_DIR / "composition_meta_by_event.csv")
    legends = pd.read_csv(OUT_DIR / "legend_pick_by_event.csv")
    classes = pd.read_csv(OUT_DIR / "legend_class_share_by_event.csv")
    weapon_categories = pd.read_csv(OUT_DIR / "weapon_category_by_event.csv")
    weapons = pd.read_csv(OUT_DIR / "weapon_meta_by_event.csv")
    reset = pd.read_csv(OUT_DIR / "reset_signal_by_event.csv")
    styles = pd.read_csv(OUT_DIR / "team_style_summary.csv")

    rows = []
    for event_slug in EVENT_ORDER:
        comp_row = concentration[concentration["event_slug"] == event_slug].iloc[0]
        event_comps = comps[comps["event_slug"] == event_slug].sort_values("pick_rate_pct", ascending=False)
        non_top5 = event_comps.iloc[5:]
        event_legends = legends[legends["event_slug"] == event_slug].sort_values("pick_rate_pct", ascending=False)
        event_classes = classes[classes["event_slug"] == event_slug].sort_values(
            "pick_rate_pct_sum", ascending=False
        )
        event_weapon_categories = weapon_categories[
            ~weapon_categories["category"].isin(["Ordnance", "Other", "Pistol/SMG", "Pistol/Akimbo"])
            & (weapon_categories["event_slug"] == event_slug)
        ].sort_values("kill_share_pct", ascending=False)
        event_weapons = weapons[
            ~weapons["category"].isin(["Ordnance", "Other"])
            & (weapons["event_slug"] == event_slug)
        ].sort_values("kill_share_pct", ascending=False)
        reset_row = reset[reset["event_slug"] == event_slug].iloc[0]
        style_rows = styles[styles["event_slug"] == event_slug].copy()
        style_total = style_rows["teams"].sum()
        style_rows["team_share_pct"] = 100 * style_rows["teams"] / style_total

        top_legend = event_legends.iloc[0]
        top_class = event_classes.iloc[0]
        top_category = event_weapon_categories.iloc[0]
        top_weapon = event_weapons.iloc[0]
        concentration_type = classify_concentration(
            float(comp_row["top1_pick_rate_pct"]),
            float(comp_row["top3_pick_rate_pct_sum"]),
            float(comp_row["top5_pick_rate_pct_sum"]),
        )

        legend_pick = {
            row["legend"]: float(row["pick_rate_pct"])
            for _, row in event_legends[event_legends["legend"].isin(
                ["Bangalore", "Bloodhound", "Caustic", "Crypto", "Wattson", "Gibraltar", "Newcastle", "Rampart", "Mad Maggie"]
            )].iterrows()
        }
        weapon_pick = {
            row["weapon"]: float(row["kill_share_pct"])
            for _, row in event_weapons[event_weapons["weapon"].isin(
                ["HAVOC Rifle", "Hemlok", "Mozambique (Akimbo)", "Mastiff Shotgun", "Peacekeeper"]
            )].iterrows()
        }

        row = {
            "event_slug": event_slug,
            "composition_count": int(comp_row["composition_count"]),
            "top1_composition": comp_row["top1_composition"],
            "top1_composition_pct": float(comp_row["top1_pick_rate_pct"]),
            "top3_composition_pct": float(comp_row["top3_pick_rate_pct_sum"]),
            "top5_composition_pct": float(comp_row["top5_pick_rate_pct_sum"]),
            "top1_to_top3_gap_pct": float(comp_row["top3_pick_rate_pct_sum"] - comp_row["top1_pick_rate_pct"]),
            "top3_to_top5_gap_pct": float(comp_row["top5_pick_rate_pct_sum"] - comp_row["top3_pick_rate_pct_sum"]),
            "non_top5_composition_count": int(len(non_top5)),
            "non_top5_weighted_top5_rate_pct": weighted_mean(non_top5, "top_5_rate_pct"),
            "non_top5_weighted_win_rate_pct": weighted_mean(non_top5, "win_rate_pct"),
            "concentration_type": concentration_type,
            "top_legend": top_legend["legend"],
            "top_legend_pick_rate_pct": float(top_legend["pick_rate_pct"]),
            "dominant_class": top_class["class"],
            "dominant_class_slot_pct": float(top_class["pick_rate_pct_sum"]),
            "support_slot_pct": float(event_classes.loc[event_classes["class"] == "Support", "pick_rate_pct_sum"].sum()),
            "recon_slot_pct": float(event_classes.loc[event_classes["class"] == "Recon", "pick_rate_pct_sum"].sum()),
            "controller_slot_pct": float(event_classes.loc[event_classes["class"] == "Controller", "pick_rate_pct_sum"].sum()),
            "bangalore_pick_rate_pct": legend_pick.get("Bangalore", 0.0),
            "bloodhound_pick_rate_pct": legend_pick.get("Bloodhound", 0.0),
            "caustic_pick_rate_pct": legend_pick.get("Caustic", 0.0),
            "crypto_pick_rate_pct": legend_pick.get("Crypto", 0.0),
            "wattson_pick_rate_pct": legend_pick.get("Wattson", 0.0),
            "gibraltar_pick_rate_pct": legend_pick.get("Gibraltar", 0.0),
            "newcastle_pick_rate_pct": legend_pick.get("Newcastle", 0.0),
            "rampart_pick_rate_pct": legend_pick.get("Rampart", 0.0),
            "mad_maggie_pick_rate_pct": legend_pick.get("Mad Maggie", 0.0),
            "top_weapon_category": top_category["category"],
            "top_weapon_category_kill_share_pct": float(top_category["kill_share_pct"]),
            "top_weapon_category_damage_share_pct": float(top_category["damage_share_pct"]),
            "top_weapon": top_weapon["weapon"],
            "top_weapon_kill_share_pct": float(top_weapon["kill_share_pct"]),
            "top_weapon_damage_share_pct": float(top_weapon["damage_share_pct"]),
            "top_weapon_fwr_pct": float(top_weapon["fwr_pct"]) if pd.notna(top_weapon["fwr_pct"]) else float("nan"),
            "havoc_kill_share_pct": weapon_pick.get("HAVOC Rifle", 0.0),
            "hemlok_kill_share_pct": weapon_pick.get("Hemlok", 0.0),
            "mozambique_akimbo_kill_share_pct": weapon_pick.get("Mozambique (Akimbo)", 0.0),
            "mastiff_kill_share_pct": weapon_pick.get("Mastiff Shotgun", 0.0),
            "peacekeeper_kill_share_pct": weapon_pick.get("Peacekeeper", 0.0),
            "deaths_per_game": float(reset_row["deaths_per_game"]),
            "respawns_per_game": float(reset_row["respawns_per_game"]),
            "revives_per_game": float(reset_row["revives_per_game"]),
            "deaths_above_60": float(reset_row["deaths_above_60"]),
            "edge_team_share_pct": style_metric(style_rows, "edge_fighting_proxy", "team_share_pct"),
            "edge_ppg": style_metric(style_rows, "edge_fighting_proxy", "avg_total_ppg"),
            "zone_team_share_pct": style_metric(style_rows, "zone_control_proxy", "team_share_pct"),
            "zone_ppg": style_metric(style_rows, "zone_control_proxy", "avg_total_ppg"),
            "hybrid_team_share_pct": style_metric(style_rows, "hybrid_high_yield", "team_share_pct"),
            "hybrid_ppg": style_metric(style_rows, "hybrid_high_yield", "avg_total_ppg"),
            "low_unstable_team_share_pct": style_metric(style_rows, "low_yield_or_unstable", "team_share_pct"),
            "low_unstable_ppg": style_metric(style_rows, "low_yield_or_unstable", "avg_total_ppg"),
        }
        row["overall_risk_level"] = classify_overall_risk(
            row["concentration_type"],
            row["top_legend_pick_rate_pct"],
            row["dominant_class_slot_pct"],
            row["top_weapon_category_kill_share_pct"],
            row["top_weapon_kill_share_pct"],
            row["revives_per_game"],
            row["respawns_per_game"],
        )
        if row["top_weapon_category"] == "Shotgun" and row["support_slot_pct"] >= 150:
            row["weapon_role_binding_proxy"] = "shotgun_defensive_reset_proxy"
        elif row["top_weapon_category"] == "AR" and (row["havoc_kill_share_pct"] + row["hemlok_kill_share_pct"]) >= 45:
            row["weapon_role_binding_proxy"] = "ar_stability_core_proxy"
        elif row["mozambique_akimbo_kill_share_pct"] >= 25:
            row["weapon_role_binding_proxy"] = "akimbo_ruleset_proxy"
        else:
            row["weapon_role_binding_proxy"] = "no_single_binding_proxy"
        rows.append(row)

    flags = pd.DataFrame(rows)
    write(flags, "operational_balance_flags_by_event.csv")

    recommendations = [
        {
            "event_slug": "playoffs_split1",
            "event_label": "Split 1 Playoffs",
            "action_level": "调优",
            "primary_risk": "信息 / 烟雾 / 控场协同让旧阵容成为稳定答案",
            "operational_judgment": "阵容和角色都高度集中，应优先拆组合收益，而不是只看 Bangalore 单点强度。",
            "optional_tuning_direction": "检查 Bloodhound 扫描与穿烟、Digital Threat、Caustic 控场的叠加收益；给非扫描和非烟雾阵容留下信息入口。",
            "evidence": "Bangalore 88.6%, Bloodhound 87.0%, Caustic 57.8%, Top 1 阵容 53.2%",
        },
        {
            "event_slug": "midseason_ewc_split1",
            "event_label": "EWC",
            "action_level": "预警",
            "primary_risk": "阵容被打散后，AR / HAVOC / Hemlok 接管输出核心",
            "operational_judgment": "职业队没有停在多样化，而是迁移到更稳定的武器答案；这是替代集中风险。",
            "optional_tuning_direction": "优先看 HAVOC / Hemlok 的稳定性、有效距离、弹药经济和伤害转击杀效率，同时恢复近战武器的明确使用场景。",
            "evidence": "AR 67.7%, HAVOC 33.9%, Hemlok 21.1%, Top 1 阵容 18.2%",
        },
        {
            "event_slug": "playoffs_split2",
            "event_label": "Split 2 Playoffs",
            "action_level": "调优",
            "primary_risk": "AR 被打散后，Akimbo / Crypto / 防守阵容形成新集中",
            "operational_judgment": "Shockwave 的方向有效，但部分信号生效过头；需要同时看武器强度和信息刚需。",
            "optional_tuning_direction": "对 Mozambique Akimbo 先查爆发窗口、拾取稳定性和有效距离；对 Crypto 优先补替代信息路径和反制反馈，而不是直接大削。",
            "evidence": "Mozambique Akimbo 33.2%, Crypto 71.5%, Top 3 阵容 65.7%",
        },
        {
            "event_slug": "championship_split2",
            "event_label": "Championship",
            "action_level": "赛事规则介入 + 系统调优",
            "primary_risk": "Support / 防守 / Shotgun / reset 形成最高确定性闭环",
            "operational_judgment": "这不是单个角色或单把枪的问题，而是失败成本被压低后，职业队缺少真实替代路径。",
            "optional_tuning_direction": "优先降低双 Support 容错和 Dome / Shield / 掩体链路稳定性，增加进攻破盾与反重置入口；赛事侧可用 Ban/Pick 打断整组最优解。",
            "evidence": "Gibraltar 99.8%, Newcastle 95.8%, Support 202.3%, Top 1 阵容 65.7%, Shotgun 65.0%",
        },
    ]
    write(pd.DataFrame(recommendations), "operational_recommendation_matrix.csv")


def main() -> None:
    score_metrics()
    reset_signal_metrics()
    team_style_metrics()
    legend_and_composition_metrics()
    weapon_metrics()
    operational_balance_metrics()
    print(f"Wrote second-layer metrics to {OUT_DIR}")


if __name__ == "__main__":
    main()
