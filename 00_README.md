# ALGS Year 4 版本运营数据分析投递包

这是一份面向游戏运营 / 数据运营岗位的作品集。核心问题是：Apex Legends 的版本更新如何改变 ALGS 职业赛场的角色、武器、阵容和打法选择；职业赛场暴露出的风险，又应该如何转化为版本运营监控和调优建议。

## 数据与版权说明

本项目是非商业求职作品集，用于展示游戏运营 / 数据分析能力。

分析基于公开 ALGS 赛事统计数据和公开 Apex Legends 版本更新信息。Apex Legends、ALGS、Electronic Arts、Respawn 及相关名称、标识归其权利方所有。本项目与 EA、Respawn、ALGS 或 Apex Legends Status 无官方关联，也不代表官方观点。

原始数据仅用于分析和复现。如数据来源方要求调整引用、移除数据或修改署名，我会及时处理。

## 包内文件

| 目录 | 内容 | 用途 |
|---|---|---|
| `report/` | 最终报告 `.docx`、飞书导出的 `.pdf`、本地 Markdown 版 | 投递、阅读和二次编辑 |
| `notebook/` | 可复现 Jupyter Notebook 及其输出 | 展示数据来源、校验、指标计算和图表生成过程 |
| `notebook/outputs/tables/` | Notebook 生成的 CSV 表格 | 复核报告中的表格和关键中间结果 |
| `notebook/outputs/figures/` | Notebook 生成的 PNG 图表 | 复核报告中的 5 张核心 dashboard |
| `notebook/outputs/intermediate/` | 清洗后的中间结果 | 方便追踪每一步数据如何得到 |
| `data/raw/portfolio_algs_year4/` | 正式原始抓取数据 | 复现分析的基础数据，不建议改动 |
| `data/processed/analysis_outputs/` | 早期分析脚本生成的正式指标表 | 报告写作和图表生成的辅助数据 |
| `figures/report_figures/` | 报告正文使用过的图表版本 | 保留报告资产 |
| `src/` | 抓取、指标计算、报告资产生成脚本和依赖列表 | 代码追溯与后续扩展 |

## 数据来源

原始数据来自公开赛事统计页面，主要是 Apex Legends Status 的 ALGS Year 4 赛事页面，以及公开 patch notes / 版本更新信息。正式数据统一保存在：

- `data/raw/portfolio_algs_year4/`

核心表包括：

- `match_scores.csv`：每局每队排名分、击杀分、总分。
- `game_team_stats.csv`：每局每队 deaths、rez、rspn、knocks 等统计。
- `overview_composition_meta.csv`：赛事级阵容组合 pick rate、Top 5、胜率等。
- `overview_legend_meta.csv`：赛事级角色 pick rate、Top 5、胜率等。
- `weapon_stats.csv`：武器击杀、伤害、击倒等。
- `patch_notes_items.csv` / `event_patch_context.csv`：版本更新与赛事窗口的对应关系。

## 运行 Notebook

在本文件夹或项目根目录中打开：

`notebook/reproduce_algs_year4_metrics.ipynb`

按顺序运行全部单元格即可。Notebook 会自动识别两种目录结构：

- 项目根目录：`data/portfolio_algs_year4/`
- 投递包目录：`data/raw/portfolio_algs_year4/`

运行后会重新生成：

- `notebook/outputs/tables/data_quality_summary.csv`
- `notebook/outputs/tables/table1_score_reset.csv` 到 `table5_team_style_ppg.csv`
- `notebook/outputs/tables/risk_flags_by_event.csv`
- `notebook/outputs/figures/fig1_score_reset_dashboard.png` 到 `fig5_team_style_ppg.png`
- `notebook/outputs/intermediate/*.csv`

## 数据限制

公开数据不包含完整路线、坐标、圈型、交战事件和队伍实时决策。因此，报告里的队伍打法分类不是路线还原，而是 proxy：

- 用队伍击杀分占比衡量是否更依赖击杀。
- 用 Top 5 率衡量是否能把运营转化为后期位置。
- 用赛事内中位数把队伍分为 `edge_fighting_proxy`、`hybrid_high_yield`、`zone_control_proxy` 和 `low_yield_or_unstable`。

这组分类适合做运营层面的宏观判断，但不能替代逐局录像复盘或完整事件流分析。

## 复核口径

Notebook 中会检查：

- 四次赛事局数是否为 Split 1=62、EWC=43、Split 2=64、Championship=69。
- `match_scores.csv` 是否有 4,760 行，即 238 局 × 20 队。
- 每局队伍数量是否为 20。
- `total_points` 是否能由 `kills + placement_points_reported` 解释。
- 阵容记录是否由 3 个 legend 组成。

已知数据质量提醒：逐局阵容表中 EWC 有 40 行阵容为空，Notebook 会在 `data_quality_summary.csv` 中标记为 warning。报告中的阵容集中度使用赛事级 `overview_composition_meta.csv`，不直接依赖这 40 行逐局阵容。

## 关键结论对应文件

- 总分与 reset 信号：`notebook/outputs/tables/table1_score_reset.csv`
- 阵容集中度：`notebook/outputs/tables/table2_composition_concentration.csv`
- 武器生态迁移：`notebook/outputs/tables/table3_weapon_share.csv`
- 单武器核对榜：`notebook/outputs/tables/table3_single_weapon_leaderboard.csv`
- 职业槽位：`notebook/outputs/tables/table4_class_slots.csv`
- 打法 proxy：`notebook/outputs/tables/table5_team_style_ppg.csv`
- 版本运营风险标志：`notebook/outputs/tables/risk_flags_by_event.csv`

## 建议阅读顺序

1. 先看 `report/ALGS Year 4 版本运营数据分析.docx`。
2. 再打开 notebook，检查数据校验和 5 张图的复现过程。
3. 如果需要追溯原始字段，再查看 `data/raw/portfolio_algs_year4/README_DATA.md` 和对应 CSV。
