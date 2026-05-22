# ALGS Year 4 Portfolio Dataset

数据目录：`data/portfolio_algs_year4`

抓取脚本：`../../algs_scraper.py`

数据来源主要为 Apex Legends Status 的 ALGS 页面。当前数据覆盖 ALGS Year 4 四个全球赛事：

- `playoffs_split1`: ALGS Year 4 Split 1 Playoffs
- `midseason_ewc_split1`: Esports World Cup / Midseason event
- `playoffs_split2`: ALGS Year 4 Split 2 Playoffs
- `championship_split2`: ALGS Year 4 Championship

## 核心文件

- `events.csv`: 赛事清单、时间、官网/统计页 URL、地图池摘要。
- `event_context.csv`: 四个赛事的日期、地点、赛制摘要、来源链接、地图池摘要。
- `event_patch_context.csv`: 赛事与对应大版本 patch notes 的映射关系。
- `event_games.csv`: 每一局比赛的索引表，包含赛事、阶段、组别、地图、game id、统计页 URL。
- `match_scores.csv`: 每场 match 的 20 支队伍排名、击杀分、总分、排名分校验结果。
- `weapon_stats.csv`: 枪械统计，包含赛事总览层级和逐局层级数据。
- `patch_notes_sources.csv`: 四个大版本 patch notes 的标题、发布时间、简介、来源链接。
- `patch_notes_items.csv`: patch notes 正文条目，按标题、段落、列表项拆分。
- `overview_team_stats.csv`: 赛事总览维度的队伍统计。
- `overview_legend_meta.csv`: 赛事总览维度的角色选择/表现统计。
- `overview_composition_meta.csv`: 赛事总览维度的阵容组合统计。
- `game_team_stats.csv`: 逐局队伍统计。
- `game_player_stats.csv`: 逐局选手统计。
- `game_legend_meta.csv`: 逐局角色统计。
- `game_composition_meta.csv`: 逐局阵容组合统计。

## 校验结果

- 赛事数：4
- 比赛局数：238
- 队伍比分行数：4,760，即 `238 * 20`
- `match_scores.csv` 中 `score_check=ok` 的行数：4,760
- 每局比分行数不是 20 的 game 数：0
- 枪械统计行数：7,216
- Patch notes 来源数：4
- Patch notes 正文条目数：1,427

## 地图池快照

- `playoffs_split1`: Storm Point 31 局，World's Edge 31 局
- `midseason_ewc_split1`: Storm Point 18 局，World's Edge 19 局，Kings Canyon 2 局，Broken Moon 2 局，Olympus 2 局
- `playoffs_split2`: World's Edge 33 局，Storm Point 31 局
- `championship_split2`: E-District 23 局，Storm Point 23 局，World's Edge 23 局

## 建议的作品集分析切入

- 版本/地图池变化如何影响武器与角色 meta。
- 队伍总分拆解：排名分导向 vs 击杀分导向。
- 阵容组合与进入前五、吃鸡、平均排名之间的关系。
- 枪械输出结构：击杀、伤害、命中率、交战距离与赛事阶段的变化。
- 强队和中游队伍的打法差异：稳定拿排名分还是高风险拿击杀分。
