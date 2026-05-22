#!/usr/bin/env python3
"""Scrape ALGS Year 4 data from Apex Legends Status.

The script is intentionally conservative:
- it uses a small request delay and local cache by default;
- it only reads public pages/endpoints;
- it writes analysis-ready CSV files under an output directory.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import http.client
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, build_opener

from lxml import html


BASE_URL = "https://apexlegendsstatus.com"
WEAPON_STATS_URL = f"{BASE_URL}/algs/local/getWeaponsStats.php"

DEFAULT_EVENTS = [
    {
        "event_slug": "playoffs_split1",
        "event_name": "ALGS Year 4 Split 1 Playoffs",
        "overview_url": f"{BASE_URL}/algs/Y4-Split1/ALGS-Playoffs/Global/Overview",
    },
    {
        "event_slug": "midseason_ewc_split1",
        "event_name": "ALGS Year 4 Midseason Playoffs / EWC",
        "overview_url": f"{BASE_URL}/algs/Y4-Split1/EWC/Global/Overview",
    },
    {
        "event_slug": "playoffs_split2",
        "event_name": "ALGS Year 4 Split 2 Playoffs",
        "overview_url": f"{BASE_URL}/algs/Y4-Split2/ALGS-Playoffs/Global/Overview",
    },
    {
        "event_slug": "championship_split2",
        "event_name": "ALGS Year 4 Championship",
        "overview_url": f"{BASE_URL}/algs/Y4-Split2/ALGS-Championships/Global/Overview",
    },
]

EVENT_CONTEXT = {
    "playoffs_split1": {
        "start_date": "2024-05-02",
        "end_date": "2024-05-05",
        "location": "Los Angeles, United States",
        "format_summary": "40 teams; group stage, bracket stage, and match point finals.",
        "source_url": "https://algs.ea.com/en/year-4/split-1-2024/news/year-4-split-1-playoffs-eyntk",
    },
    "midseason_ewc_split1": {
        "start_date": "2024-07-31",
        "end_date": "2024-08-04",
        "location": "Riyadh, Saudi Arabia",
        "format_summary": "40 teams; Esports World Cup Apex Legends event with group and finals stages.",
        "source_url": "https://liquipedia.net/apexlegends/Esports_World_Cup/2024",
    },
    "playoffs_split2": {
        "start_date": "2024-08-29",
        "end_date": "2024-09-01",
        "location": "Mannheim, Germany",
        "format_summary": "40 teams; group stage, bracket stage, and match point finals.",
        "source_url": "https://algs.ea.com/en/year-4/split-2-2024/news/algs-year-4-split-2-playoffs-dates-venue",
    },
    "championship_split2": {
        "start_date": "2025-01-29",
        "end_date": "2025-02-02",
        "location": "Sapporo, Japan",
        "format_summary": "40 teams; group stage, bracket stage, and match point finals.",
        "source_url": "https://algs.ea.com/en/year-4/champs-2025/competition-overview",
    },
}

PATCH_NOTE_SOURCES = [
    {
        "patch_slug": "breakout",
        "patch_name": "Breakout",
        "source_url": "https://www.ea.com/games/apex-legends/apex-legends/news/breakout-patch-notes",
    },
    {
        "patch_slug": "upheaval",
        "patch_name": "Upheaval",
        "source_url": "https://www.ea.com/games/apex-legends/apex-legends/news/upheaval-patch-notes",
    },
    {
        "patch_slug": "shockwave",
        "patch_name": "Shockwave",
        "source_url": "https://www.ea.com/games/apex-legends/apex-legends/news/shockwave-patch-notes",
    },
    {
        "patch_slug": "from_the_rift",
        "patch_name": "From The Rift",
        "source_url": "https://www.ea.com/games/apex-legends/apex-legends/news/from-the-rift-season-updates",
    },
]

EVENT_PATCH_CONTEXT = [
    {
        "event_slug": "playoffs_split1",
        "patch_slug": "breakout",
        "relationship": "Closest major season patch before Split 1 Playoffs.",
    },
    {
        "event_slug": "midseason_ewc_split1",
        "patch_slug": "upheaval",
        "relationship": "Closest major season patch before the midseason EWC event.",
    },
    {
        "event_slug": "playoffs_split2",
        "patch_slug": "shockwave",
        "relationship": "Closest major season patch before Split 2 Playoffs.",
    },
    {
        "event_slug": "championship_split2",
        "patch_slug": "from_the_rift",
        "relationship": "Closest major season patch before Year 4 Championship.",
    },
]

PLACEMENT_POINTS = {
    1: 12,
    2: 9,
    3: 7,
    4: 5,
    5: 4,
    6: 3,
    7: 3,
    8: 2,
    9: 2,
    10: 2,
    11: 1,
    12: 1,
    13: 1,
    14: 1,
    15: 1,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
}


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def slugify_header(value: str, fallback: str) -> str:
    value = clean_text(value)
    value = value.replace("%", " pct")
    value = value.replace("->", " to ")
    value = value.replace("=>", " to ")
    value = value.replace("→", " to ")
    value = value.replace("/", " per ")
    value = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return value or fallback


def to_int(value: Any) -> int | None:
    text = clean_text(value).replace(",", "")
    if not text or text.upper() in {"NAN", "NA", "N/A", "-"}:
        return None
    match = re.search(r"-?\d+", text)
    return int(match.group(0)) if match else None


def to_float(value: Any) -> float | None:
    text = clean_text(value).replace(",", "").replace("%", "")
    if not text or text.upper() in {"NAN", "NA", "N/A", "-"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


class Fetcher:
    def __init__(self, cache_dir: Path, sleep_seconds: float, refresh_cache: bool = False):
        self.cache_dir = cache_dir
        self.sleep_seconds = sleep_seconds
        self.refresh_cache = refresh_cache
        self.opener = build_opener()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_text(self, url: str) -> str:
        cache_path = self.cache_dir / f"get_{sha1_text(url)}.html"
        if cache_path.exists() and not self.refresh_cache:
            return cache_path.read_text(encoding="utf-8")
        body = self._request(url)
        text = body.decode("utf-8", errors="replace")
        cache_path.write_text(text, encoding="utf-8")
        return text

    def post_json(self, url: str, data: dict[str, Any], referer: str | None = None) -> Any:
        encoded = urlencode({k: "" if v is None else v for k, v in data.items()})
        cache_key = f"{url}?{encoded}"
        cache_path = self.cache_dir / f"post_{sha1_text(cache_key)}.json"
        if cache_path.exists() and not self.refresh_cache:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        body = self._request(
            url,
            data=encoded.encode("utf-8"),
            extra_headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Referer": referer or BASE_URL,
            },
        )
        text = body.decode("utf-8", errors="replace")
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            preview = text[:500].replace("\n", " ")
            raise RuntimeError(f"Expected JSON from {url}, got: {preview}") from exc
        cache_path.write_text(json.dumps(parsed, ensure_ascii=False), encoding="utf-8")
        return parsed

    def _request(
        self,
        url: str,
        data: bytes | None = None,
        extra_headers: dict[str, str] | None = None,
        max_attempts: int = 4,
    ) -> bytes:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "close",
        }
        if extra_headers:
            headers.update(extra_headers)

        last_error: Exception | None = None
        for attempt in range(1, max_attempts + 1):
            try:
                if self.sleep_seconds > 0:
                    time.sleep(self.sleep_seconds)
                req = Request(url, data=data, headers=headers)
                with self.opener.open(req, timeout=45) as response:
                    return response.read()
            except (HTTPError, URLError, TimeoutError, OSError, http.client.HTTPException) as exc:
                last_error = exc
                if attempt == max_attempts:
                    break
                time.sleep(min(2 * attempt, 8))
        raise RuntimeError(f"Failed to fetch {url}: {last_error}") from last_error


@dataclass
class GameInfo:
    event_slug: str
    event_name: str
    split: str
    league: str
    region: str
    day: str
    group: str
    stage: str
    game_label: str
    game_number: int | None
    map_name: str
    game_id: str
    stats_url: str
    replay_url: str
    title: str


def parse_algs_path(url: str) -> dict[str, str]:
    parts = urlparse(url).path.strip("/").split("/")
    parsed = {
        "split": "",
        "league": "",
        "region": "",
        "day": "",
        "group": "",
        "game_id": "",
    }
    if len(parts) >= 4 and parts[0] == "algs":
        parsed["split"] = parts[1]
        parsed["league"] = parts[2]
        parsed["region"] = parts[3]
    if len(parts) >= 5:
        parsed["day"] = parts[4]
    if len(parts) >= 6:
        parsed["group"] = parts[5]
    if len(parts) >= 7:
        parsed["game_id"] = parts[6]
    return parsed


def parse_js_vars(page_text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for name in ["league", "split", "region", "day", "group", "gameId"]:
        match = re.search(rf"\b(?:let|const|var)\s+{name}\s*=\s*['\"]([^'\"]*)", page_text)
        if match:
            result[name] = match.group(1)
    return result


def parse_game_title(title: str) -> tuple[str, str, int | None, str]:
    title = clean_text(title)
    match = re.match(r"(.+?)\s+-\s+(Game\s+#(\d+))\s+-\s+(.+)$", title)
    if not match:
        return "", "", None, ""
    return match.group(1), match.group(2), int(match.group(3)), match.group(4)


def discover_games(event: dict[str, str], page_text: str) -> list[GameInfo]:
    doc = html.fromstring(page_text)
    seen: set[str] = set()
    games: list[GameInfo] = []

    for link in doc.xpath('//a[contains(normalize-space(.), "View game stats")]'):
        href = link.get("href")
        if not href:
            continue
        stats_url = urljoin(event["overview_url"], href)
        path_info = parse_algs_path(stats_url)
        game_id = path_info["game_id"]
        if not game_id or game_id in seen:
            continue
        seen.add(game_id)

        title_bits = link.xpath('preceding::h3[contains(@class,"replay-banner_title")][1]//text()')
        title = clean_text(" ".join(title_bits))
        stage, game_label, game_number, map_name = parse_game_title(title)
        replay_url = f"{BASE_URL}/algs/game/{game_id}"

        games.append(
            GameInfo(
                event_slug=event["event_slug"],
                event_name=event["event_name"],
                split=path_info["split"],
                league=path_info["league"],
                region=path_info["region"],
                day=path_info["day"],
                group=path_info["group"],
                stage=stage,
                game_label=game_label,
                game_number=game_number,
                map_name=map_name,
                game_id=game_id,
                stats_url=stats_url,
                replay_url=replay_url,
                title=title,
            )
        )

    return sorted(games, key=game_sort_key)


def game_sort_key(game: GameInfo) -> tuple[str, str, int, str]:
    number = game.game_number if game.game_number is not None else 9999
    return (game.day, game.group, number, game.game_id)


def parse_score_matrix(page_text: str, game: GameInfo) -> list[dict[str, Any]]:
    doc = html.fromstring(page_text)
    tables = doc.xpath('//table[contains(concat(" ", normalize-space(@class), " "), " score-matrix_table ")]')
    if not tables:
        return []

    rows: list[dict[str, Any]] = []
    for tr in tables[0].xpath(".//tbody/tr"):
        cells = [clean_text(" ".join(cell.xpath(".//text()"))) for cell in tr.xpath("./td")]
        if len(cells) < 5:
            continue
        score_rank = to_int(cells[0])
        team = cells[1]
        total_points = to_int(cells[2])
        placement = to_int(cells[3])
        kills = to_int(cells[4])
        if not team or placement is None or kills is None or total_points is None:
            continue
        placement_points_reported = total_points - kills
        placement_points_rule = PLACEMENT_POINTS.get(placement)
        rows.append(
            {
                **game.__dict__,
                "score_rank": score_rank,
                "team": team,
                "placement": placement,
                "kills": kills,
                "total_points": total_points,
                "placement_points_reported": placement_points_reported,
                "placement_points_rule": placement_points_rule,
                "score_check": (
                    "ok"
                    if placement_points_rule is None or placement_points_rule == placement_points_reported
                    else "mismatch"
                ),
            }
        )
    return rows


def table_to_rows(table: html.HtmlElement) -> tuple[list[str], list[dict[str, str]]]:
    all_rows = table.xpath(".//tr")
    if not all_rows:
        return [], []
    header_cells = all_rows[0].xpath("./th|./td")
    headers_raw = [clean_text(" ".join(cell.xpath(".//text()"))) for cell in header_cells]
    headers: list[str] = []
    used: dict[str, int] = {}
    for idx, header in enumerate(headers_raw, start=1):
        key = slugify_header(header, f"col_{idx}")
        if key in used:
            used[key] += 1
            key = f"{key}_{used[key]}"
        else:
            used[key] = 1
        headers.append(key)

    parsed_rows: list[dict[str, str]] = []
    for tr in all_rows[1:]:
        values = [clean_text(" ".join(cell.xpath(".//text()"))) for cell in tr.xpath("./td|./th")]
        if not values or not any(values):
            continue
        row: dict[str, str] = {}
        for idx, value in enumerate(values):
            key = headers[idx] if idx < len(headers) else f"extra_col_{idx + 1}"
            row[key] = value
        parsed_rows.append(row)
    return headers, parsed_rows


def classify_table(headers: list[str], rows: list[dict[str, str]] | None = None) -> str:
    header_set = set(headers)
    first = headers[0] if headers else ""
    first_values = [row.get(first, "") for row in (rows or []) if first]
    looks_like_composition = any("," in value for value in first_values[:10])
    if first == "legend" and "total_occurrences" in header_set:
        return "composition_meta" if looks_like_composition else "legend_meta"
    if first in {"legend", "composition"} and "games_played" in header_set:
        if first == "legend" and looks_like_composition:
            return "composition_by_scope"
        return f"{first}_by_scope"
    if first == "composition" and "total_occurrences" in header_set:
        return "composition_meta"
    if first == "team" and "total_pts" in header_set:
        return "team_stats"
    if first == "player" and "team" in header_set and "kills" in header_set:
        return "player_stats"
    if first == "weapon" and "kills" in header_set and "damage" in header_set:
        return "weapon_table"
    if first == "poi":
        return "poi_stats"
    if first == "team" and "total" in header_set:
        return "team_map_stats"
    if first == "player" and any("ring" in h or "loot" in h for h in headers):
        return "player_timing_stats"
    return "other"


def nearest_heading(table: html.HtmlElement) -> str:
    headings = table.xpath("preceding::*[self::h1 or self::h2 or self::h3 or self::h4][normalize-space()][last()]")
    if not headings:
        return ""
    return clean_text(" ".join(headings[0].xpath(".//text()")))


def collect_tables(page_text: str, metadata: dict[str, Any], source_scope: str) -> dict[str, list[dict[str, Any]]]:
    doc = html.fromstring(page_text)
    buckets: dict[str, list[dict[str, Any]]] = {}
    raw_rows: list[dict[str, Any]] = []

    for table_index, table in enumerate(doc.xpath("//table")):
        classes = f" {table.get('class') or ''} "
        if " score-matrix_table " in classes:
            continue
        headers, rows = table_to_rows(table)
        if not headers or not rows:
            continue
        table_type = classify_table(headers, rows)
        heading = nearest_heading(table)

        for row_number, row in enumerate(rows, start=1):
            if table_type.startswith("composition") and "legend" in row and "composition" not in row:
                row = {**row, "composition": row["legend"]}
                del row["legend"]
            enriched = {
                **metadata,
                "source_scope": source_scope,
                "table_index": table_index,
                "table_type": table_type,
                "table_heading": heading,
                "row_number": row_number,
                **row,
            }
            raw_rows.append(enriched)
            buckets.setdefault(table_type, []).append(enriched)

    buckets["raw_table_rows"] = raw_rows
    return buckets


def weapon_rows_from_api(
    data: dict[str, Any],
    metadata: dict[str, Any],
    source_scope: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for weapon_key, payload in data.items():
        if not isinstance(payload, dict):
            continue
        meta = payload.get("meta") or {}
        knockdowns = to_int(payload.get("knockdowns"))
        times_knocked = to_int(payload.get("timesKnocked"))
        fwr_pct: float | None = None
        if knockdowns is not None and times_knocked is not None and knockdowns + times_knocked > 0:
            fwr_pct = round(100 * knockdowns / (knockdowns + times_knocked), 2)
        rows.append(
            {
                **metadata,
                "source_scope": source_scope,
                "weapon_key": weapon_key,
                "weapon": meta.get("name") or weapon_key,
                "kills": payload.get("kills"),
                "damage": payload.get("damage"),
                "knockdowns": payload.get("knockdowns"),
                "times_knocked": payload.get("timesKnocked"),
                "fwr_pct": fwr_pct,
                "shots": payload.get("shots"),
                "hits": payload.get("hits"),
                "accuracy": payload.get("accuracy"),
                "playtime": payload.get("playtime"),
                "playtime_seconds": payload.get("playtimeSeconds"),
                "max_kill_range": payload.get("maxKillRange"),
                "max_damage_range": payload.get("maxDamageRange"),
                "icon": meta.get("icon"),
            }
        )
    return rows


def fetch_weapon_rows(
    fetcher: Fetcher,
    params: dict[str, Any],
    metadata: dict[str, Any],
    source_scope: str,
    referer: str,
) -> list[dict[str, Any]]:
    api_data = fetcher.post_json(WEAPON_STATS_URL, params, referer=referer)
    if not isinstance(api_data, dict):
        return []
    return weapon_rows_from_api(api_data, metadata, source_scope)


def event_overview_weapon_params(page_text: str, overview_url: str) -> dict[str, str]:
    js_vars = parse_js_vars(page_text)
    path_info = parse_algs_path(overview_url)
    return {
        "league": js_vars.get("league") or path_info["league"],
        "split": js_vars.get("split") or path_info["split"],
        "region": js_vars.get("region") or path_info["region"],
        "day": js_vars.get("day") or "Overview",
        "group": js_vars.get("group") or "NONE",
        "playerId": "anyPlayer",
        "ringStage": "0",
        "rangeBucket": "ANY",
        "gameId": js_vars.get("gameId") or "",
    }


def game_weapon_params(page_text: str, game: GameInfo) -> dict[str, str]:
    js_vars = parse_js_vars(page_text)
    return {
        "league": js_vars.get("league") or game.league,
        "split": js_vars.get("split") or game.split,
        "region": js_vars.get("region") or game.region,
        "day": js_vars.get("day") or game.day,
        "group": js_vars.get("group") or game.group,
        "playerId": "anyPlayer",
        "ringStage": "0",
        "rangeBucket": "ANY",
        "gameId": js_vars.get("gameId") or game.game_id,
    }


def extend_bucket(target: dict[str, list[dict[str, Any]]], source: dict[str, list[dict[str, Any]]]) -> None:
    for key, rows in source.items():
        target.setdefault(key, []).extend(rows)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    if not fieldnames:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def map_pool(games: list[GameInfo]) -> str:
    maps = sorted({game.map_name for game in games if game.map_name})
    return ", ".join(maps)


def first_xpath_text(doc: html.HtmlElement, xpath: str) -> str:
    values = doc.xpath(xpath)
    if not values:
        return ""
    if isinstance(values, str):
        return clean_text(values)
    return clean_text(values[0])


def article_content_rows(
    page_text: str,
    metadata: dict[str, Any],
    source_kind: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    doc = html.fromstring(page_text)
    root = (doc.xpath("//main") or [doc])[0]
    title = first_xpath_text(doc, "string(//h1)") or first_xpath_text(doc, "string(//title)")
    published_at = first_xpath_text(doc, "string(//meta[@property='article:published_time']/@content)")
    description = (
        first_xpath_text(doc, "string(//meta[@name='description']/@content)")
        or first_xpath_text(doc, "string(//meta[@property='og:description']/@content)")
    )
    source_row = {
        **metadata,
        "source_kind": source_kind,
        "title": title,
        "published_at": published_at,
        "description": description,
    }

    rows: list[dict[str, Any]] = []
    current_h2 = ""
    current_h3 = ""
    current_h4 = ""
    content_nodes = root.xpath(".//*[self::h2 or self::h3 or self::h4 or self::p or self::li or self::tr]")

    for item_index, node in enumerate(content_nodes, start=1):
        tag = node.tag.lower()
        if tag == "tr":
            cells = [clean_text(" ".join(cell.xpath(".//text()"))) for cell in node.xpath("./th|./td")]
            text = " | ".join(cell for cell in cells if cell)
        else:
            text = clean_text(" ".join(node.xpath(".//text()")))
        if not text:
            continue
        if tag == "h2":
            current_h2 = text
            current_h3 = ""
            current_h4 = ""
        elif tag == "h3":
            current_h3 = text
            current_h4 = ""
        elif tag == "h4":
            current_h4 = text

        rows.append(
            {
                **metadata,
                "source_kind": source_kind,
                "item_index": item_index,
                "item_type": tag,
                "section_h2": current_h2,
                "section_h3": current_h3,
                "section_h4": current_h4,
                "text": text,
            }
        )
    return source_row, rows


def event_context_rows(
    events: list[dict[str, str]],
    discovered_rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    discovered_by_slug = {row.get("event_slug"): row for row in (discovered_rows or [])}
    rows: list[dict[str, Any]] = []
    for event in events:
        context = EVENT_CONTEXT.get(event["event_slug"], {})
        discovered = discovered_by_slug.get(event["event_slug"], {})
        rows.append(
            {
                **event,
                **context,
                "game_count_discovered": discovered.get("game_count_discovered", ""),
                "game_count_scraped": discovered.get("game_count_scraped", ""),
                "map_pool_discovered": discovered.get("map_pool_discovered", ""),
            }
        )
    return rows


def write_context_outputs(
    out_dir: Path,
    fetcher: Fetcher,
    events: list[dict[str, str]],
    discovered_event_rows: list[dict[str, Any]] | None = None,
) -> dict[str, int]:
    if discovered_event_rows is None:
        discovered_event_rows = read_csv_rows(out_dir / "events.csv")
    event_context = event_context_rows(events, discovered_event_rows)
    write_csv(out_dir / "event_context.csv", event_context)

    event_slugs = {event["event_slug"] for event in events}
    patch_slugs = {
        row["patch_slug"]
        for row in EVENT_PATCH_CONTEXT
        if row["event_slug"] in event_slugs
    }
    selected_patch_sources = [row for row in PATCH_NOTE_SOURCES if row["patch_slug"] in patch_slugs]
    selected_event_patch_context = [
        row for row in EVENT_PATCH_CONTEXT if row["event_slug"] in event_slugs and row["patch_slug"] in patch_slugs
    ]

    patch_sources: list[dict[str, Any]] = []
    patch_items: list[dict[str, Any]] = []
    for patch in selected_patch_sources:
        print(f"[context] fetching patch notes - {patch['patch_slug']}")
        page_text = fetcher.get_text(patch["source_url"])
        source_row, rows = article_content_rows(page_text, patch, "patch_notes")
        patch_sources.append(source_row)
        patch_items.extend(rows)

    write_csv(out_dir / "event_patch_context.csv", selected_event_patch_context)
    write_csv(out_dir / "patch_notes_sources.csv", patch_sources)
    write_csv(out_dir / "patch_notes_items.csv", patch_items)

    summary = {
        "event_context_rows": len(event_context),
        "event_patch_context_rows": len(selected_event_patch_context),
        "patch_note_sources": len(patch_sources),
        "patch_note_items": len(patch_items),
    }
    (out_dir / "context_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


def scrape(args: argparse.Namespace) -> dict[str, int]:
    out_dir = Path(args.out_dir)
    fetcher = Fetcher(Path(args.cache_dir), args.sleep, refresh_cache=args.refresh_cache)
    selected = set(args.events or [event["event_slug"] for event in DEFAULT_EVENTS])
    events = [event for event in DEFAULT_EVENTS if event["event_slug"] in selected]

    if args.context_only:
        return write_context_outputs(out_dir, fetcher, events)

    event_rows: list[dict[str, Any]] = []
    all_games: list[dict[str, Any]] = []
    all_scores: list[dict[str, Any]] = []
    weapons: list[dict[str, Any]] = []
    overview_tables: dict[str, list[dict[str, Any]]] = {}
    game_tables: dict[str, list[dict[str, Any]]] = {}

    for event in events:
        print(f"[event] {event['event_slug']} - fetching overview")
        overview_text = fetcher.get_text(event["overview_url"])
        games = discover_games(event, overview_text)
        if args.limit_games is not None:
            games_to_scrape = games[: args.limit_games]
        else:
            games_to_scrape = games

        path_info = parse_algs_path(event["overview_url"])
        event_rows.append(
            {
                **event,
                **path_info,
                "game_count_discovered": len(games),
                "game_count_scraped": 0 if args.only_discover else len(games_to_scrape),
                "map_pool_discovered": map_pool(games),
            }
        )
        all_games.extend([game.__dict__ for game in games])

        overview_meta = {
            **event,
            **path_info,
            "source_url": event["overview_url"],
        }
        extend_bucket(overview_tables, collect_tables(overview_text, overview_meta, "overview"))

        if not args.skip_weapons:
            print(f"[event] {event['event_slug']} - fetching overview weapon stats")
            params = event_overview_weapon_params(overview_text, event["overview_url"])
            weapons.extend(fetch_weapon_rows(fetcher, params, overview_meta, "overview", event["overview_url"]))

        if args.only_discover:
            continue

        for idx, game in enumerate(games_to_scrape, start=1):
            print(f"[game] {event['event_slug']} {idx}/{len(games_to_scrape)} - {game.title or game.game_id}")
            game_text = fetcher.get_text(game.stats_url)
            all_scores.extend(parse_score_matrix(game_text, game))

            game_meta = {
                **game.__dict__,
                "source_url": game.stats_url,
            }
            extend_bucket(game_tables, collect_tables(game_text, game_meta, "game"))

            if args.include_game_weapons and not args.skip_weapons:
                params = game_weapon_params(game_text, game)
                weapons.extend(fetch_weapon_rows(fetcher, params, game_meta, "game", game.stats_url))

    write_csv(out_dir / "events.csv", event_rows)
    write_csv(out_dir / "event_games.csv", all_games)
    write_csv(out_dir / "match_scores.csv", all_scores)
    write_csv(out_dir / "weapon_stats.csv", weapons)

    for prefix, buckets in [("overview", overview_tables), ("game", game_tables)]:
        for table_type, rows in buckets.items():
            write_csv(out_dir / f"{prefix}_{table_type}.csv", rows)

    context_summary = write_context_outputs(out_dir, fetcher, events, event_rows)

    summary = {
        "events": len(event_rows),
        "games_discovered": len(all_games),
        "games_scored": len({row["game_id"] for row in all_scores}),
        "match_score_rows": len(all_scores),
        "weapon_rows": len(weapons),
        "overview_raw_table_rows": len(overview_tables.get("raw_table_rows", [])),
        "game_raw_table_rows": len(game_tables.get("raw_table_rows", [])),
        **context_summary,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scrape ALGS Year 4 public stats from Apex Legends Status.")
    parser.add_argument(
        "--events",
        nargs="*",
        choices=[event["event_slug"] for event in DEFAULT_EVENTS],
        help="Event slugs to scrape. Defaults to all four Year 4 global events.",
    )
    parser.add_argument("--out-dir", default="data/raw/algs_year4", help="Directory for CSV outputs.")
    parser.add_argument("--cache-dir", default=".cache/algs_scraper", help="Directory for cached HTTP responses.")
    parser.add_argument("--limit-games", type=int, default=None, help="Scrape only the first N discovered games per event.")
    parser.add_argument("--sleep", type=float, default=0.35, help="Delay between requests, in seconds.")
    parser.add_argument("--refresh-cache", action="store_true", help="Ignore existing cached responses.")
    parser.add_argument("--only-discover", action="store_true", help="Only discover event games and overview tables.")
    parser.add_argument(
        "--context-only",
        action="store_true",
        help="Only write event context and patch-note context files.",
    )
    parser.add_argument("--skip-weapons", action="store_true", help="Skip the weapon stats API.")
    parser.add_argument(
        "--include-game-weapons",
        action="store_true",
        help="Also fetch weapon stats for every scraped game. This adds many API calls.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = scrape(args)
    print("\nDone.")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
