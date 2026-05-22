# ALGS Year 4 版本运营数据分析

这是一份基于 ALGS Year 4 公开数据的版本运营分析

这份报告尝试用公开数据回答一个问题：

**版本更新上线后，职业赛场到底发生了什么变化？**

我把 ALGS Year 4 的四次国际赛事作为连续观察窗口，对照官方版本更新、赛事得分、武器击杀、角色选择、阵容组合和地图池，重点看三件事：

1. 版本想改变什么
2. 职业队实际怎么响应，有没有符合设计预期
3. 这些变化是带来了更多选择，还是形成了新的集中风险。

# 1. 项目摘要

## 选择ALGS Year 4的原因

第一，我是 Apex 的长期玩家和赛事观众，累计游戏时长约 550 小时。虽然在 2024 年因为学业和个人体验变化减少了游玩时间，但我仍然持续关注版本更新和 ALGS 职业赛事。相比单纯从玩家感受出发，我更想用数据验证：版本更新到底改变了什么，职业队又是如何响应这些变化的。

第二，ALGS Year 4 是 Apex 职业生态变化非常明显的一年。版本机制、角色强度、武器环境、地图池和赛事规则都发生了较大调整，适合作为一个连续观察窗口，分析版本更新如何影响高水平竞技环境。

我没有选择 ALGS Year 5 作为主要分析对象，是因为 Year 5 引入了 Legend Bans 等新规则，赛事环境的变量更多，分析难度会明显上升。因此，本报告先聚焦 Year 4 四次国际赛事，尝试建立一套更稳定、可复盘的版本运营分析框架。

## 核心结论

这份分析的核心结论是：**ALGS Year 4 的版本更新确实改变了职业赛场，但改变主要发生在角色、阵容和武器选择上，而不是总得分结构上。**

四次国际赛事的击杀分占比都稳定在 **51% 到 52%** 左右。这个结果并不意外：Apex 职业比赛一局有 20 支队伍、60 名选手，如果不考虑复活和非计分死亡，除了吃鸡队伍外，理论上会有接近 57 名选手被淘汰。再加上 ALGS 赛制同时奖励击杀和排名，击杀分占比本身就不容易出现剧烈波动。

每次版本更新后，职业队都会迅速寻找当前版本最稳定的组合，并把它推到极限：

- **Upheaval 后**，旧的 Bangalore / Bloodhound / Caustic 阵容被打散，但 HAVOC / Hemlok / AR 接管了武器生态。
- **Shockwave 后**，AR 统治被打破，Akimbo Mozambique 和 Shotgun 成为新的近战核心。
- **From The Rift 后**，Support / 防守重置 体系极端收敛，Gibraltar + Newcastle 几乎成为刚需。

因此，我认为版本运营需要关注的不只是“强势角色或武器有没有被削弱”，还要持续追踪：

**旧 meta 被处理后，新的高确定性组合是否正在形成。**

这也是后续分析的重点：把版本更新、职业赛场响应和生态集中风险放在一起观察。

# 2. 游戏机制与职业赛场背景

## Apex 的强度不是单点强弱，而是组合收益

Apex 的职业生态不是由单个角色或单把枪决定的，它更像三层系统叠在一起。

第一层是 BR 规则：20 支队伍同场，安全区持续压缩，队伍需要同时处理资源、转移、交战和终局位置。ALGS 又同时计算击杀分和排名分，所以职业队不能只追求击杀，也不能只追求存活。

第二层是角色阵容：Apex 的队伍由 3 个角色组成，强度经常来自组合。信息、控场、防守、机动、治疗、复活和资源能力会互相叠加。职业端不会孤立地问“某角色强不强”，而是会问“这个角色能不能稳定提高整套阵容的胜率和容错”。

第三层是武器交战：武器强度也不能脱离角色和地图。远中距离武器影响消耗和空间压制，Shotgun / SMG / Akimbo 影响近战收割和终局决胜，LMG / Gun Shield / 掩体技能则可能改变阵地防守时的正面对抗收益。

所以这份报告不做孤立的“角色榜”或“枪械榜”，而是分析：

**版本更新是否改变了角色、武器、地图和打法之间的组合收益。**

## ALGS 得分结构如何塑造打法

职业比赛里常见两类宏观打法

**早进圈控点**更重视提前进圈、占据高价值地形、用信息和防守技能降低转移风险，再把位置优势转化为后期排名分和终局击杀。它不是“苟分”，因为高水平控点队伍最终仍然要靠终局收割扩大分差。

**圈边推进**更重视资源发育、护甲成长、清边击杀和逐步进圈。它也不是“无脑打架”，因为如果击杀不能转化成 Top 5 或胜场，总分收益会很低。

因此我在第二层分析里没有直接断言某队“真实早进圈”或“真实圈边”。公开数据不足以还原每支队伍的完整路线，我使用的是可解释的代理指标：



| **打法画像** | **代理指标** | **解释** |
|-|-|-|
| 早进圈控点倾向 | 排名分占比高、Top 5 率高、击杀分占比相对低 | 更像依靠位置和稳定后期转化拿分 |
| 圈边推进倾向 | 击杀分占比高、场均击杀高、Top 5 率偏低 | 更像依靠清边和团战拿分，但风险更高 |
| 混合适应型 | 击杀分占比高、Top 5 率也高 | 既能打出击杀，也能把击杀带进后期 |



## 职业赛场为什么适合做版本压力测试

普通玩家环境里，一个强势机制可能会被娱乐性、熟练度、随机队友和个人偏好稀释。但职业队不会等版本慢慢发酵，他们会很快做三件事：

1. 找到当前版本最高确定性的阵容。
2. 找到当前版本最稳定的武器组合。
3. 把地图、落点、转移、角色和武器绑定成可重复执行的体系。

所以职业赛场更容易暴露版本生态里的集中风险：

- 单一角色接近必选；
- Top 1 阵容覆盖率过高；
- 某个武器类别接管击杀来源；
- 某种打法同时最稳、最能打、最能拿分；
- 替代阵容缺少真实竞争力。

## 赛制本身信号

版本更新不是唯一影响职业生态的东西，赛事规则也会改变比赛环境。

Year 4 Split 2 Pro League 起，ALGS 引入 POI Draft。队伍不再完全依赖传统跳伞抢点，而是在规则框架内选择落点。这个变化会降低无意义落地碰撞，让比赛更关注中后期决策、路线规划、资源利用和阵容适配。

赛场不是被动接受版本更新，它也会通过暴露最优解，反过来推动赛事规则和版本系统迭代。

# 3. 数据范围与方法

## 赛事范围



| **赛事** | **日期** | **地点** | **赛制概况** | **地图池** | **已抓取局数** |
|-|-|-|-|-|-|
| ALGS Year 4 Split 1 Playoffs | 2024-05-02 至 2024-05-05 | Los Angeles | 40 队，组赛、淘汰赛、赛点制决赛 | Storm Point, World's Edge | 62 |
| ALGS Year 4 Midseason Playoffs / EWC | 2024-07-31 至 2024-08-04 | Riyadh | 40 队，EWC Apex 项目，含小组与决赛阶段 | Broken Moon, Kings Canyon, Olympus, Storm Point, World's Edge | 43 |
| ALGS Year 4 Split 2 Playoffs | 2024-08-29 至 2024-09-01 | Mannheim | 40 队，组赛、淘汰赛、赛点制决赛 | Storm Point, World's Edge | 64 |
| ALGS Year 4 Championship | 2025-01-29 至 2025-02-02 | Sapporo | 40 队，组赛、淘汰赛、赛点制决赛 | E-District, Storm Point, World's Edge | 69 |



## 使用的数据

本项目使用的是公开数据，不追求复刻官方后台，也不假装拥有公开数据之外的信息。

- 官方 patch notes：用于提取版本设计信号。
- 赛事 match score：每场比赛的队伍排名分、击杀分、总分。
- 武器统计：武器击杀、伤害、使用时长等。
- 角色与阵容数据：pick rate、阵容组合、Top 5 转化等。
- 地图池与比赛地图：用于检查地图变化是否影响整体得分结构。

完整事件流数据当然更理想，例如坐标、路线、换枪、击杀事件和交战距离。但考虑复杂程度，当前这组数据已经足够支撑版本运营分析，而且结论更容易复算和解释。

## 核心指标



| **指标** | **计算方式** | **用途** |
|-|-|-|
| 击杀分占比 | kills / total_points | 判断比赛整体更偏击杀收益还是排名收益 |
| 排名分 | total_points - kills | 拆分总分结构，并用 ALGS 规则校验 |
| 每局总击杀 | 赛事总击杀 / 比赛局数 | 观察版本是否提高整体交战强度 |
| Top 5 率 | top_5s / games | 衡量队伍进入后期的稳定性 |
| PPG | total_points / games | 比较不同打法画像的平均收益 |
| 阵容集中度 | Top 1 / Top 3 / Top 5 阵容 pick rate 之和 | 判断阵容是否收敛到少数最优解 |
| 职业类别槽位占比 | 每队 3 个角色槽位相加 | 例如 Support 202.3% 表示平均每队约两个 Support 角色槽位 |
| 武器类别击杀占比 | 某类主武器击杀 / 全部主武器击杀 | 判断武器生态是否被某一距离或类别接管 |



这些指标不能替代完整事件流，但它们有一个优点：稳定、可解释、可复算，适合作为版本后监控的第一层口径。

# 4. 第一层：版本更新想改变什么

这一层不直接讨论职业赛场结果，而是先做一层**版本意图假设**。

我不会把公开 patch notes 直接等同于设计师的真实意图。我们能看到的是版本调整方向，不能证明设计师内部具体怎么想。因此，这一层的目的不是“替官方解释版本”，而是把版本更新拆成可以被后续数据验证的信号。

我把三次赛事间版本更新拆成三组：

- Upheaval：Split 1 Playoffs -> EWC。
- Shockwave：EWC -> Split 2 Playoffs。
- From The Rift：Split 2 Playoffs -> Championship。

## Upheaval：打散旧协同，但不保证自然多样化

在分析 Upheaval 时，我没有把它理解成一次单纯的数值调整，而是把它看成一次对旧版本稳定体系的拆解。

Split 1 阶段，职业赛场最典型的稳定答案是 **Bangalore / Bloodhound / Caustic**。这套阵容强，不是因为三个角色单独强，而是因为它们组合在一起后覆盖了职业比赛里非常关键的几个需求：Bangalore 提供烟雾和交战空间，Bloodhound 提供扫描信息，Caustic 提供终局控场。再加上 30-30、Wingman、Digital Threat 等稳定强势点，整套体系的确定性很高。

因此，我把 Upheaval 的版本信号拆成三类来看。

**第一，削弱旧环境里的稳定强势点。**  
 30-30、Wingman、Digital Threat 等调整，会直接影响中远距离消耗、烟雾环境下的信息优势，以及职业队稳定拿输出的方式。我的验证假设是：如果 30-30 下降后，其他 Marksman / Sniper 能获得更多空间，说明武器生态确实变得更分散；但如果职业队只是转向 HAVOC、Hemlok 或其他 AR，那么这次更新可能只是把集中点从一个武器体系转移到了另一个武器体系。

**第二，降低开局随机性和资源波动。**  
 未持枪时打开补给箱至少获得一把低等级武器，说明版本希望减少极端落地劣势。不过公开数据看不到完整的落地过程，也看不到每支队伍的实时搜刮路线，所以这部分不能直接下结论。后续只能用低排名低击杀、高击杀低排名、单局低分等代理指标，间接观察开局波动是否有所缓和。

**第三，重排角色协同和地图资源。**  
 Bloodhound、Caustic、Catalyst、Crypto、Fuse、Newcastle、Wattson 等角色调整，加上 Broken Moon、World’s Edge、Storm Point 的资源点、Ring Console、Survey Beacon 和 Crafter 刷新变化，都会影响队伍的转移、控点和终局处理方式。这里我关注的不是某个角色单独变强或变弱，而是旧的“烟雾 + 扫描 + 控场”结构是否会失去稳定性。

所以 Upheaval 的核心假设是：

**旧的 Bangalore / Bloodhound / Caustic 结构会被打散，但职业队可能会寻找新的稳定输出中心。**

## Shockwave：重塑信息、控点和交战距离

相比 Upheaval，Shockwave 的版本信号更直接。我的理解是，这次更新不是单纯调整几把武器或几个角色，而是在重新分配职业比赛里的几个核心价值：**谁负责控点，谁负责拿信息，队伍应该在什么距离完成击杀。**

我把 Shockwave 的信号拆成三类。

**第一，强化圈内站位和控点收益。**  
 Controller 获得 Zone Overcharge，在圈内可以获得额外护盾容量。这个改动给出的信号很明确：版本在奖励提前进圈、占住位置、利用地形和防守技能打后期的队伍。  
 所以我后续会观察 Controller 角色是否上升，以及早进圈控点型队伍的收益有没有提高。

**第二，Recon 从全图信息转向战术信息。**  
 Survey Beacon 不再提供全图扫描，而是改为范围脉冲；Recon 获得 ADS Threat Vision。我的理解是，Recon 的定位从“提前知道全局队伍分布”，变成了更偏近中距离的信息确认。  
 这会影响职业队的清边、转移安全和开团判断。因此我后续重点看的是：Crypto 等 Recon 角色是否会接住信息位，以及信息角色是否会和控点、防守角色形成新的固定组合。

**第三，压低 AR 稳定输出，扶持近中距离爆发。**  
 Shockwave 削弱了 Havoc、Hemlok 等稳定输出点，同时加入 Akimbo P2020 / Mozambique，提高 Shotgun 一致性，并让 LMG 获得 Gun Shield Generator。这个方向很明显：版本在降低 Energy / Heavy 中远距离稳定收益，同时给 Light、Shotgun、LMG 和 Akimbo 更多上场空间。  
 所以我想验证的是：AR 统治是否会被打破；如果被打破，武器生态会真正分散，还是会转向新的 Akimbo / Shotgun 集中。

另外，E-District 虽然在 Shockwave 中登场，但 Split 2 Playoffs 的地图池仍然是 Storm Point 和 World’s Edge。因此这一张新地图对职业赛场的影响，需要放到 Championship 阶段再观察，不能提前归因。

所以，Shockwave 阶段我的核心假设是：

**职业赛场会从 HAVOC / Hemlok / AR 的稳定输出环境，转向更依赖战术信息、圈内控点和近中距离爆发的环境。**

但这里也有一个需要警惕的点：  
**如果 AR 被削弱后，Akimbo 或 Shotgun 很快接管击杀来源，那么这次更新可能不是让武器生态变得更分散，而是把集中风险从中远距离转移到了近距离。**

## From The Rift：建立 Support 身份，但可能放大防守重置体系

From The Rift 的版本信号非常集中。和 Upheaval、Shockwave 相比，这次更新给我的感觉不是“让某些角色变强一点”，而是在重新定义 Support 在队伍里的价值，或者说这是一次真正意义上的游戏职业划分，这样职业划分这个行为更有意义和影响。

过去 Support 更多是功能性位置，但 From The Rift 之后，Support 开始直接影响团战后的恢复速度和容错率。Heal Expert、Revive Expert、小药治疗量提升、复活速度提升、复活后生命恢复，这些改动都在强化同一个方向：**让队伍在打完一波团之后，更快完成 reset，并重新回到可战斗状态。**

我把 From The Rift 的信号拆成三类来看。

**第一，Support 的队伍价值明显上升。**  
 Support 获得治疗和复活相关强化后，职业队很可能会优先测试它能不能提高团战后的容错。这里我想验证的是：Support 角色是否会从“可选功能位”变成“职业队固定携带的核心槽位”，甚至出现双 Support 阵容。

**第二，防守重置角色被进一步强化。**  
 Gibraltar、Newcastle、Wattson 等角色都和防守、复活、掩体、拖时间有关。Gibraltar 的 Dome 冷却降低且更难被反制，Newcastle 的 Mobile Shield 和复活盾收益提高，Wattson 也能获得 Revive Expert。  
 这些改动叠在一起后，职业队可能会更倾向于选择能“保护倒地队友、拖住交战节奏、重新组织站位”的阵容。后续我会重点观察 Gibraltar / Newcastle 是否成为高 pick 组合，以及它们是否和 Rampart、Shotgun 等形成固定体系。

**第三，限制难以反制的信息优势。**  
 Crypto 的 Drone 开始受到圈伤，Off the Grid 增加可见和可听反馈。这个方向说明版本在降低不可交互信息的价值。我的验证假设是：Crypto 在 Split 2 的高使用率可能会被压下去，但职业队不会因此放弃稳定性，而是可能把角色槽位转向 Support 和防守重置。

武器方面，Havoc 进入 Care Package，L-STAR、Longbow、Spitfire、Sentinel、Peacekeeper、Triple Take 等也有调整。这里我不会只看单把枪的强弱，而会重点看武器是否和角色体系绑定。例如，如果 Gibraltar Dome、Newcastle Shield、Rampart 掩体让交战更多发生在近距离和掩体边缘，那么 Shotgun 的击杀占比可能会被防守重置体系一起推高。

所以，From The Rift 阶段我的核心假设是：

**Support / 防守重置体系会明显上升，Crypto 等信息角色会下降；但如果治疗、复活、Dome、Shield 和掩体叠加后容错率过高，职业队可能会迅速收敛到少数阵地阵容。**

这也是这一阶段最需要警惕的地方：  
**版本成功建立了 Support 身份，但也可能让“打完能重置、倒人能救回、终局能拖住”的阵容变得过于稳定。**

## 总结

看完三次版本更新后，我的判断是：ALGS Year 4 的版本更新并不是简单地鼓励“更多打架”，也不是单纯鼓励“更早进圈”。

更准确地说，版本在同时强化两类能力。

一类是**阵地能力**。  
 Controller 的圈内护盾收益、Support 的治疗和复活强化、Gibraltar Dome、Newcastle Shield、Rampart 掩体、LMG Gun Shield 等改动，都在提高队伍占点、防守、拖时间和团战后恢复的能力。这会让早进圈控点队伍更容易把位置优势转化成后期收益。

另一类是**主动交战能力**。  
 Recon 的战术信息、Shotgun / Akimbo 的近战爆发、Crypto 等信息角色的确认能力，以及 Support 带来的团战后重置，都在提高队伍清边、开团和连续作战的容错。这会让圈边推进队伍更容易把击杀转化成后期排名。

所以，第二层真正要验证的不是“某个角色或某把枪有没有变强”，而是：

**这些版本信号有没有改变职业队选择角色、武器、阵容和打法的方式。**

如果版本更新只是让职业队从一个最优解迁移到另一个最优解，那么它确实改变了 meta，但不一定带来了更健康的多样化。

# 5. 第二层：分析数据，职业赛场发生了什么改变

先说结论：

**有改变，而且响应改变强；但改变主要发生在武器、角色和阵容选择上，总得分结构依旧很稳定。**

## 图表 1：总击杀稳定，但 reset 信号上升



![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MmYzZmVmMDVkOWU5YTMzM2EyZjAwOWI3YjA2YzlhNzlfYTIwY2IxMzFiOGE5NTBjOTg1OTc5Mjk0MmE1ZDJlYzRfSUQ6NzY0MTkwNjAzMTQxMjc5MjI5Ml8xNzc5NDM3MDk0OjE3Nzk0NDA2OTRfVjM)

*Score and reset signal dashboard*



这张图不是想说明“版本更新让比赛多了多少击杀”，而是想把三个容易混在一起的概念拆开看：**计分击杀、实际死亡，以及重生 / 救起带来的 reset 空间。**

从计分击杀来看，四次赛事都非常稳定。每局计分击杀基本维持在 **56–58** 左右，击杀分占比也稳定在 **51%–52%**。这和大逃杀规则本身有关：Apex 职业赛一局有 60 名选手，如果不考虑复活，除了吃鸡队伍 3 人外，理论上最多会有 57 人被淘汰。所以，计分击杀天然不会出现特别夸张的波动。



| 赛事 | 场数 | 计分击杀 / 局 | 死亡 / 局 | 重生 rspn / 局 | 救起 rez / 局 | 击杀分占比 |
|-|-|-|-|-|-|-|
| Split 1 Playoffs | 62 | 56.4 | 59.8 | 2.7 | 8.8 | 51.1% |
| EWC | 43 | 56.6 | 58.2 | 2.4 | 9.8 | 51.2% |
| Split 2 Playoffs | 64 | 57.6 | 60.1 | 3.9 | 10.3 | 51.6% |
| Championship | 69 | 57.4 | 60.9 | 3.8 | 19.4 | 51.5% |



数据口径：计分击杀来自每局比分表，代表队伍真正拿到的击杀分；死亡、rspn 和 rez 来自每局队伍统计。

**死亡、重生和救起不能直接等同于额外击杀**。胜队可能会减员，倒地后可能被救起，复活后的玩家也可能再次死亡，毒圈和环境伤害也会造成非计分死亡。

真正值得关注的是 reset 指标：Split 2 和 Championship 的场均重生从前两站的 2.4–2.7 抬到 3.8–3.9，Championship 的场均救起进一步跳到 19.4。

这说明版本没有显著改变总击杀池，但提高了队伍在减员、倒地和换血失败后的继续运营能力。版本影响不是“每局多打很多架”，而是“队伍失败一次之后更不容易直接出局”。

单看总击杀会低估版本影响。Split 2 更像是 Crypto 带来的远程拿牌、信息避战和重启机会；Championship 则更像 Gibraltar / Newcastle / Rampart 体系带来的倒地救援、掩体换血和终局容错。后面的分析要继续看角色、阵容、武器和打法收益，因为版本影响往往先体现在这些更敏感的层面。

## 图表 2：阵容集中度先被打散，又重新收敛



![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTlmNmFhMGRmZjNlZDAzMjExNmY5ZGRmNDhjY2U3NzBfMTEwOTNiMjgzODM5YjQ1NDNmYWY3ODJiODRmZGZhM2JfSUQ6NzY0MTkwNjA0ODY0MjkyNzU2NF8xNzc5NDM3MDkzOjE3Nzk0NDA2OTNfVjM)

*Composition concentration dashboard*



阵容集中度的变化非常清楚：



| **赛事** | **主流 Top 1 阵容** | **Top 1 覆盖率** | **Top 3 覆盖率** | **Top 5 覆盖率** |
|-|-|-|-|-|
| Split 1 | Bangalore, Bloodhound, Caustic | 53.2% | 70.2% | 79.1% |
| EWC | Bangalore, Pathfinder, Wattson | 18.2% | 47.7% | 71.1% |
| Split 2 | Bangalore, Crypto, Wattson | 36.7% | 65.7% | 79.4% |
| Championship | Gibraltar, Newcastle, Rampart | 65.7% | 91.5% | 97.4% |



- Top 1 覆盖率：本次赛事里，使用次数最多的那套三人阵容，占全部“队伍-单局阵容记录”的比例。
- Top 3 覆盖率：使用次数最多的前三套阵容，加起来占全部阵容记录的比例。
- Top 5 覆盖率：使用次数最多的前五套阵容，加起来占全部阵容记录的比例。



阵容集中度比单个角色 pick rate 更能说明职业赛场的变化。因为 Apex 的强度通常不是由单个角色决定的，而是由三人阵容的组合收益决定的：信息、转移、防守、控场、复活和终局处理，会一起决定一套阵容是否稳定。



**阵容不是凭空变化的，Top 1 阵容变化背后其实是职业分工的重新洗牌。**



具体看，阵容集中度不能只读成“阵容变多或变少”。更关键的是：每次 Top 1 阵容变化，都对应了版本对职业分工的重新分配。

先看 Split 1 的 Bangalore / Bloodhound / Caustic。这套阵容强，不是因为三个角色孤立地强，而是它们把当时职业比赛最需要的三件事合在了一起：Bangalore 提供烟雾和交战空间，Bloodhound 提供低成本信息和开团判断，Caustic 负责终局控场。换句话说，Bloodhound以及Digital Threat在这套阵容里承担的是“稳定信息”的位置，尤其适合和 Bangalore 的烟雾环境绑定。

Upheaval 后，Bloodhound 消失得很快，核心原因不是职业队突然不需要信息，而是这套信息体系的确定性被削弱了。版本提高了 Bloodhound 大招冷却，并取消击倒延长大招时间；同时 Digital Threat、30-30、Wingman 等旧环境里的稳定强势点也被处理。原本围绕烟雾、扫描、中远距离消耗和控场构成的旧答案被拆开后，Bloodhound 的角色价值就不再是不可替代的。结果也很直接：Bloodhound pick rate 从 87.0% 降到 10.6%，Split 1 的 Top 1 阵容覆盖率从 53.2% 降到 EWC 的 18.2%。

所以 Upheaval 的设计目标在“打散旧阵容”这件事上是实现了的。但它没有让职业赛场自然走向长期多样化。职业队或许只是进入了一段试错期，然后继续寻找下一个稳定答案。

这也解释了为什么“职业分工”比单个角色强弱更重要。Bloodhound 不是单纯被某个角色替代，而是他的原岗位被版本拆开了：一部分信息价值被 Crypto 接走，一部分转移和控点价值被 Pathfinder / Wattson 接走，到了 Championship，职业队甚至认为“信息位”不如“双 Support + 防守锚点”重要。

**我的结论：**

**版本更新能打散旧 meta，但不会自动带来长期多样化。职业队会继续寻找下一套最稳定、最容易复制的标准答案。**

## 图表 3：武器生态发生了三次迁移



![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZjYyNDUzZGFkYzQ3MWNmZmQxYzBlNWQ1NjVjZmEyMDBfNTNjYTlhMWRkY2FiMzNiZWU1M2I0NmM2Nzg1ZjQ3MWRfSUQ6NzY0MTkwNjA2MzU1MzcxMTA3MF8xNzc5NDM3MDkzOjE3Nzk0NDA2OTNfVjM)

*Weapon shift dashboard*

武器类别的迁移比总得分结构剧烈得多：

- Split 1：AR 57.5%，SMG 23.3%，Precision 10.3%。
- EWC：AR 升到 67.7%，HAVOC 和 Hemlok 成为核心。
- Split 2：AR 降到 33.1%，Shotgun/Akimbo 升到 34.3%，Mozambique Akimbo 单武器占 33.2%。
- Championship：Shotgun 升到 65.0%，Precision 升到 20.4%，AR 降到 12.0%。



这说明版本更新确实改变了职业队的武器选择，但这张图不能简单理解成“某把枪被削了，所以职业队换枪了”。

在 Apex 职业赛场里，武器选择经常不是独立发生的，而是被角色体系和交战环境牵引出来的。换句话说，版本直接改枪只是第一层；真正落到比赛里，会变成：

**角色分工改变 → 交战距离改变 → 武器选择改变。**

Split 1 的环境下，Bangalore + Bloodhound 让烟雾和扫描形成稳定信息优势，队伍既能中距离消耗，也能在确认信息后贴近打架；Caustic 又强化终局控场。因此 AR 和 SMG 都有明确位置。

Upheaval 后，Bloodhound 扫描体系被打散，职业队更依赖转移、站位和中距离稳定输出。Pathfinder 提供路线和进退，Wattson 提供圈内防守，结果 AR 的稳定压制价值被放大，HAVOC / Hemlok 成为新的输出中心。

Shockwave 后，HAVOC / Hemlok 被压下去，Akimbo 和 Shotgun 得到加强。但更关键的是，Crypto 接住了信息位。队伍能通过信息确认敌人位置，再用 Bangalore 和 Wattson 管理交战空间，近距离爆发武器就更容易完成收割。因此，Mozambique Akimbo 的上升不只是武器强度问题，也和信息体系带来的近战决策稳定性有关。

到了 Championship，Gibraltar / Newcastle / Rampart 把比赛进一步推向防守重置和终局近战。Dome、Mobile Shield、Rampart 掩体让很多团战变成“掩体后换血”和“贴脸进出掩体”的节奏，Shotgun 自然成为最适配的终局武器。Precision 则负责远中距离消耗和压制，为防守阵地创造安全输出。



我的结论是：

**AR 集中 → Akimbo / Shotgun 集中 → Shotgun + Precision 集中，并不是三次孤立的武器轮换，而是三次角色体系改变交战距离的结果。**

这也解释了为什么 Championship 的 Shotgun 65.0% 特别值得警惕。它不只是 Shotgun 本身强，而是 Support、Dome、Shield、Rampart 掩体和终局空间一起，把职业比赛推向了 Shotgun 最舒服的交战距离。

从运营角度看，如果后续只削弱单把 Shotgun，可能处理不了根因。真正需要监控的是：**防守重置体系是否持续把职业队锁进同一种近战决胜环境。**



## 图表 4：角色职业槽位暴露版本需求



![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YjI4NmVkZmExODQzMzE4OGVkY2NhNzlhMWIyNmIxNjZfZjIwMGQ3MzkxYzJmY2M0NGFlNzQ4YjVkMmYwZTBiYWRfSUQ6NzY0MTkwNjA3OTU1MDQ1ODgyMV8xNzc5NDM3MDkzOjE3Nzk0NDA2OTNfVjM)

*Legend class slots dashboard*



职业类别槽位的读法需要注意：它把每队 3 个角色槽位相加，所以最高理论值是 300%。

最明显的变化是 Championship：

- Support 槽位合计 202.3%，意味着平均每队约两个 Support 槽位。
- Recon 从 Split 2 的 71.6% 降到几乎 0。
- Assault 从 Split 2 的 93.9% 降到 0.8%。

这不是普通 pick rate 波动，更像职业端对版本需求的一次集体投票：

**From The Rift 后，职业队几乎一致认为 Support / 控制 / 防守体系比信息、机动或突击 输出更值得投入角色槽位。**

## 图表 5：纯圈边击杀不是最高收益



![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDZlNmVjYzdmOGY4MjQ2Y2IyMWRkNzg3ZjY3YTM5MzVfODFkMzA2ZDI0MmU0NDQ5ZGIyMmYxMDYwMDUyZGE2MWZfSUQ6NzY0MTkwNjA5MjA4Mzc0MzcxMF8xNzc5NDM3MDk0OjE3Nzk0NDA2OTRfVjM)

*Team style PPG dashboard*

队伍打法画像的 PPG 更能说明职业比赛的底层逻辑。由于公开数据没有完整路线、坐标、搜刮和交战事件，我不能直接判断每支队伍是真正的“早进圈”还是“圈边推进”。

我用了两个口径看打法变化，但这里需要注意：前一个口径适合做“队伍画像”，不适合直接当成真实路线比例。

- **队伍画像占比**：每个赛事中，多少队更像圈边推进、早进圈控点、混合高收益或低收益不稳定。
- **单局结果占比**：每个 team-game 里，出现了多少“高击杀 Top 5”“高击杀低排名”“低击杀 Top 5”这类结果。

队伍画像的计算方式是：在每个赛事内部，分别取队伍击杀分占比和 Top 5 率的中位数，再切成四类：

- 击杀分占比高、Top 5 率高：混合高收益型；
- 击杀分占比高、Top 5 率低：圈边推进型；
- 击杀分占比低、Top 5 率高：早进圈控点型；
- 两者都低：低收益 / 不稳定。

再看每种打法画像的平均收益：



| 风格 | Split 1 PPG | EWC PPG | Split 2 PPG | Champs PPG |
|-|-|-|-|-|
| edge_fighting_proxy | 4.54 | 4.86 | 4.34 | 4.71 |
| hybrid_high_yield | 6.80 | 5.95 | 6.72 | 6.46 |
| zone_control_proxy | 6.13 | 6.50 | 6.58 | 6.45 |
| low_yield_or_unstable | 4.11 | 3.32 | 3.57 | 4.01 |



结果比较清楚：**圈边推进型队伍的击杀分占比更高，但平均 PPG 始终低于混合高收益型和早进圈控点型。**

这说明 ALGS 并不奖励“只有击杀、没有后期”的打法。职业比赛里的高收益路径，通常不是单纯多打架，而是能不能把击杀带进 Top 5，把团战收益转化成排名分和终局击杀。

如果进一步看单局结果，这个结论会更明显：



| 单局结果代理 | Split 1 | EWC | Split 2 | Champs |
|-|-|-|-|-|
| 低击杀 Top 5 | 2.3% | 2.6% | 2.0% | 2.3% |
| 高击杀低排名 | 2.7% | 3.1% | 2.4% | 3.6% |
| 高击杀 Top 5 | 15.0% | 13.6% | 16.2% | 15.3% |



这里最关键的是：**高击杀 Top 5 始终远高于低击杀 Top 5。**

这说明职业比赛里的“控点”并不是低击杀苟排名。真正高收益的队伍，往往是能在进入后期的同时完成击杀收割。换句话说，ALGS 的核心不是“打架还是运营”，而是能不能把击杀、存活和排名连成一条收益链。

因此，这一节我不会得出“早进圈一定比圈边好”的结论。更准确的判断是：

**版本真正影响的，不是队伍想不想打架，而是哪类阵容更容易把击杀转化成 Top 5 和终局收益。**

这也能解释为什么后续要继续看角色、阵容和武器：

 如果某套阵容既能接团、又能 reset、还能稳定进入终局，它就会比单纯高击杀打法更有版本优势。



## 第二层小结：版本更新改变了职业赛场，但没有自动带来多样化

把前面的得分结构、阵容集中度、武器生态、职业槽位和 reset 指标放在一起看，ALGS Year 4 的职业赛场确实对版本更新做出了明显响应。

但这个响应不是简单的“比赛变得更爱打架”或者“某个角色被削弱后消失”。更准确地说，职业队会根据版本变化，重新寻找当前环境下**最稳定、最容易复制、容错率最高的组合收益**。

### 结论一：版本更新会打散旧答案，但不会自动制造多样化

Upheaval 是最典型的例子。旧的 Bangalore / Bloodhound / Caustic 阵容被打散后，Bloodhound 从 87.0% 降到 10.6%，Top 1 阵容覆盖率也从 53.2% 降到 18.2%。从“打散旧阵容”这个目标看，版本是有效的。

但问题是，职业队没有长期停留在多样化阶段，而是很快寻找新的稳定答案。30-30 下降后，武器生态没有自然分散，反而转向 HAVOC / Hemlok / AR 的稳定输出体系；AR 击杀占比在 EWC 升到 67.7%，HAVOC 和 Hemlok 也成为核心输出点。

所以这里真正的运营结论不是“Upheaval 成功了”或者“Upheaval 失败了”，而是：

**削弱旧 meta 只能打开试错窗口，不能保证生态长期多样化。**

版本运营需要重点监控的是：旧答案被削弱后的 1–2 个赛事窗口里，职业队会不会迅速把新的稳定答案压缩出来。

### 结论二：职业队选择的不是单点强度，而是“低风险组合”

Shockwave 表面上是在削弱 HAVOC / Hemlok、扶持 Shotgun / Akimbo / LMG，同时调整 Recon 和 Controller。但职业赛场真正接收的不是某一条改动，而是一整套低风险组合：**战术信息 + 圈内控点 + 近战爆发**。

这就是为什么 Crypto 会从 12.5% 升到 71.5%，Newcastle 从 0.1% 升到 38.9%，同时 Shotgun / Akimbo 从 0.0% 升到 34.3%，Mozambique Akimbo 单武器击杀占比达到 33.2%。

这里的关键不是“某把枪强了”，而是 Crypto 提供信息确认，Wattson / Newcastle 提供防守和容错，Akimbo / Shotgun 提供近战终结。它们叠在一起后，让职业队更容易完成：

**发现目标 → 安全接近 → 近战爆发 → 团战后重置。**

所以 Shockwave 的价值判断要分两层：

-  第一层：它确实打破了 AR 统治，改动有效； 
-  第二层：它把集中风险从 AR 稳定输出，转移到了 Akimbo / Shotgun 和信息确认体系。 

这比“AR 下降、Shotgun 上升”更有分析价值，因为它说明：

**职业端追求的不是理论最强单点，而是能降低决策风险的组合**

### 结论三：From The Rift 的问题不是 Support 太强，而是“失败成本”被压得太低

Championship 的变化最值得警惕。Gibraltar 99.8%、Newcastle 95.8%、Support 槽位 202.3%，Gibraltar / Newcastle / Rampart 单一阵容覆盖率 65.7%，Top 3 阵容覆盖率 91.5%，Shotgun 击杀占比 65.0%。

如果只看单点，可能会得出“Gibraltar 太强”“Newcastle 太强”“Shotgun 太强”的结论。但我认为更准确的判断是：

**From The Rift 把职业队一次失误后的失败成本压得太低。**

Support 治疗和复活提高了团战后的恢复速度；Gibraltar Dome 和 Newcastle Shield 提供了安全救援窗口；Rampart 掩体提高了阵地换血能力；Shotgun 又最适合这种掩体边缘、泡泡内外、终局贴脸的交战环境。

这些机制叠加后，职业队不是单纯“更难被打死”，而是更容易在以下场景中保住比赛资格：

-  倒人后能救； 
-  换血亏了能拖； 
-  被冲脸能用 Dome / Shield 拆节奏； 
-  终局能用掩体和 Shotgun 把不确定性压低。 

所以 Championship 的真正风险不是某个角色 pick rate 高，而是：

**Support / 防守 / Shotgun 形成了一套完整的容错闭环。**

这类问题如果只削单个角色或单把枪，可能会把强势点转移到下一个替代品，而不是解决根因。



### 结论四：后两次更新让职业类别从“标签”变成阵容构建变量

 Shockwave 和 From The Rift 的共同点，是它们不再只调整单个角色，而是在强化职业类别本身的队伍职能。Shockwave 让 Recon / Controller 更明确地承担信息和控点价值；From The Rift 则让 Support 直接影响治疗、复活和团战后 reset。

从结果看，这个方向被职业队接收得很明显：Split 2 阶段 Recon / Controller 仍然有较高槽位占比，Championship 阶段 Support 槽位进一步达到 202.3%。这说明职业队不再只是挑选单个强角色，而是在围绕职业类别重新分配阵容槽位。

但这也带来风险：当某个职业类别提供过高的团队收益时，它不会只是成为“可选风格”，而会变成“必选结构”。From The Rift 的 Support 就是最明显的例子。



# 6. 第三层：版本上线后的运营监控指标系统

之前已经说明职业赛场确实发生了变化，但这些变化还不足以直接推导出平衡方案。

## 6.1 设计是否实现：版本想推的方向有没有被职业队采用

这组指标回答一个基础问题：设计师想推动的方向，职业队有没有真的接受。

比如 Shockwave 明显想重新强化职业分工，Recon、Controller 的战术价值被抬高；From The Rift 则明显强化了 Support 的 reset / recovery 身份。职业赛场如果真的响应，变化不应该只体现在某个角色突然被选，而应该体现在三人阵容结构、得分效率和终局稳定性上。



| 指标 | 观察口径 | 影响运营判断 |
|-|-|-|
| 目标职业槽位占比 | Recon、Controller、Support 是否上升 | 判断职业类别身份是否被接收 |
| 目标角色 pick rate | Crypto、Wattson、Gibraltar、Newcastle 等是否上升 | 判断被加强方向是否进入职业选择 |
| 含目标职业阵容占比 | 含 Recon、含 Controller、双 Support 阵容比例 | 判断职业类别是否从“功能标签”变成阵容结构 |
| 目标职业 Top 5 / PPG | 使用该职业的队伍是否更稳定拿分 | 判断高 pick 是真实收益，还是短期跟风 |
| 目标职业胜场占比 | 关键职业是否集中在高排名队伍中 | 判断是否形成职业刚需 |



我的判断方式会比较克制：

- 如果目标职业 pick rate 上升，但 Top 5 和 PPG 没有提升，说明版本信号被接收了，但未必构成强度问题。
- 如果目标职业 pick rate、Top 5、PPG 和阵容覆盖率同时上升，说明这个职业类别已经开始影响上分效率，需要进入重点监控。
- 如果某个被加强方向仍然没有上场，说明改动可能没有解决职业队真正需要的岗位问题。

## 6.2 环境健康程度：新标准答案或者毒瘤阵容有没有形成

职业比赛天然会追求确定性，所以阵容集中本身不一定是问题。

实际上需要更加关注层级结构：

如果 Top 1 阵容覆盖率高，但 Top 3 / Top 5 没有同步升高，说明这套阵容可能只是主流答案，职业环境里仍然存在反制阵容、地图适配阵容或队伍风格差异。这更接近“一超多强”，不一定需要立刻调数值。

但如果 Top 1 高，Top 3 / Top 5 也很高，说明问题不只是某一套阵容强，而是可竞争阵容池被压缩。尤其当 Top 5 覆盖率非常高时，即使每套阵容不同，它们也可能共享同一套底层收益，例如 Support / 防守 / Recon。

这里还有一个需要注意的点：阵容收益不能只看 PPG。

 当大多数强队都使用同一套阵容时，收益会被平均化。镜像阵容互相对抗时，胜负更多由队伍实力、落点、圈型和临场决策决定，而不是阵容差异本身。因此，判断阵容健康度时，还要看非主流阵容是否仍有进入 Top 5、拿胜场、打出高击杀局的空间。

所以我会先看一组基础指标，再根据这些指标判断集中度类型。



| 指标 | 观察口径 | 影响运营判断 |
|-|-|-|
| Top 1 阵容覆盖率 | 使用次数最多的单套阵容占比 | 单一阵容接近标准答案 |
| Top 3 阵容覆盖率 | 使用次数前三的阵容合计占比 | 可竞争阵容池明显变窄 |
| Top 5 阵容覆盖率 | 使用次数前五的阵容合计占比 | 职业生态高度收敛 |
| 单一角色 pick rate | 某个角色是否接近必选 | 角色可能承担不可替代岗位 |
| 单一职业类别槽位 | 某职业类别总槽位是否过高 | 队伍平均携带超过 1.5 个该职业 |
| Top 1 与 Top 3 差值 | Top 3 覆盖率 - Top 1 覆盖率 | 判断是“一超多强”还是单一阵容独大 |
| Top 3 与 Top 5 差值 | Top 5 覆盖率 - Top 3 覆盖率 | 判断第 4、第 5 套阵容是否还有存在感 |
| 非 Top 5 阵容 PPG / Top 5 率 | 非主流阵容的平均得分和后期转化 | 判断替代阵容是否仍有真实竞争力 |
| 地图分布差异 | 主流阵容在不同地图的覆盖率 | 判断阵容强势是全局问题还是地图限定 |



我会把集中度分成几种状态：



| 集中度类型 | 数据表现 | 可能含义 | 运营动作 |
|-|-|-|-|
| 较为平衡或者还在试错 | Top 1 低，Top 3 / Top 5 也低 | 职业队还在找答案或者该版本确实较为平衡 | 继续观察 不急于调数值 |
| 一超多强 | Top 1 高，但 Top 3 / Top 5 没有同步过高；非 Top 5 阵容仍有 Top 5 或胜场 | 有主流答案，但仍存在反制、地图适配或队伍风格差异 | 监控收益差距，不急于削弱 |
| 多核心 | Top 1 不高，但 Top 5 很高 | 表面上有多套阵容，但可竞争阵容池仍然很窄 | 检查这些阵容是否共享同一职业类别、武器 |
| 单一垄断 | Top 1 高，Top 3 / Top 5 也高；非主流阵容缺少 Top 5 和胜场 | 可竞争阵容池被压缩，职业队缺少真实选择 | 进入调优或赛事规则讨论 |



如果集中度高，并且这套阵容的 Top 5、PPG、胜场也高，那它大概率不是“职业队保守跟风”，而是已经形成真实收益。如果集中度高但收益一般，可能只是新版本不确定期的保守选择，应该继续观察，而不是马上调数值。

## 6.3 武器与交战距离：是枪太强，还是阵容把比赛推到了这把枪最舒服的位置

武器生态从 AR 集中，迁移到 Akimbo / Shotgun，再到 Championship 的 Shotgun + Precision。这个变化不能只从武器本身解释，因为 Apex 的武器选择经常被角色体系反向塑造。

比如 Gibraltar Dome、Newcastle Shield、Rampart 掩体和 Support reset 体系，会让队伍更愿意把战斗拖进近距离、可反复拉扯的空间。这样一来，Shotgun 的高击杀占比就不一定只是“霰弹枪太强”，也可能是阵容体系把职业比赛推到了霰弹枪最稳定的交战距离。



| 指标 | 观察口径 | 影响运营判断 |
|-|-|-|
| 武器类别击杀占比 | AR、Shotgun、Precision、SMG、LMG 占比 | 判断某类交战距离是否接管比赛 |
| 单一武器击杀占比 | HAVOC、Hemlok、Mozambique、Mastiff 等 | 判断是否出现单武器主导 |
| 武器伤害占比 vs 击杀占比 | 高伤害低击杀，还是低伤害高击杀 | 判断武器是消耗工具还是收割工具 |
| 武器使用时长 / 击杀参与 | 职业队是否稳定围绕某类武器打架 | 判断它是否成为默认配置 |
| 武器与阵容绑定率 | Shotgun 是否主要绑定 Gibraltar、Newcastle、Rampart | 判断问题在枪本体，还是角色体系放大了枪 |
| 地图维度武器占比 | 不同地图是否推高某类武器 | 判断是地图问题还是全局问题 |



我的判断会分两步：

- 如果某类武器击杀占比超过 50%，不能直接说这类武器一定超标。
- 如果所有阵容都使用它，更像是武器本体强度问题；如果它主要绑定某类阵容，更像是角色体系改变了交战距离。

这能解释 Championship 的情况：Shotgun 的 65% 击杀占比非常夸张，但它不是孤立出现的。它和 Gibraltar、Newcastle、Rampart、Support reset 同时集中，说明问题更像是“防守重置体系把比赛压进近战环境”，而不是单独某一把枪的问题。

## 6.4 Reset 与失败成本：队伍是不是变得太不容易出局

From The Rift 强化 Support 后，reset 指标需要被单独拿出来看。因为职业比赛里，reset 不是简单的“救起来一次”，它会改变队伍犯错后的成本。

如果一个队伍倒人之后仍然能稳定救起、重整、继续进圈，版本就可能在无形中提高了防守阵容的容错率。这个变化不一定会立刻反映在总击杀或总分结构上，但会改变终局质量和阵容选择。



| 指标 | 观察口径 | 影响运营判断 |
|-|-|-|
| 场均 rez | 每局救起次数 | 判断倒地后是否更容易恢复 |
| 场均 rspn | 每局重生次数 | 判断队伍是否更容易获得第二次机会 |
| 死亡数 - 计分击杀 | 复活后再死亡、非计分死亡、环境死亡空间 | 判断 reset 是否放大额外死亡循环 |
| Support 槽位占比 | Support 是否成为默认阵容结构 | 判断 reset 是否进入阵容核心 |
| 有 rez 队伍 Top 5 率 | 救起是否真的帮助队伍进入后期 | 判断 reset 是否转化成排名收益 |
| rspn 后得分转化 | 重生后是否还能拿分或进 Top 5 | 判断重生是有效运营资源还是象征性机会 |
| 高 reset 阵容 PPG | Gibraltar、Newcastle、Rampart 等阵容得分 | 判断 reset 体系是否形成稳定收益 |



职业比赛有救人和复活，本来就是 Apex 区别于很多大逃杀的重要机制。

真正需要警惕的是：rez / rspn 上升的同时，Support 阵容的 Top 5、PPG 和胜场也上升。如果这几项一起发生，说明失败成本被实质性降低，需要检查治疗、复活、Dome、Shield、掩体之间的组合。

如果 rez / rspn 上升，但 Top 5 和 PPG 没有提升，那它可能只是让队伍多了一些尝试机会，并没有真正破坏版本健康。

## 6.5 未接收加强：为什么被加强了还是没人选

这一组指标在判断设计信号为什么没有进入职业端。

职业队的三人阵容位非常贵。一个角色被加强，并不代表他能上场；他必须回答一个更现实的问题：他能替代谁？他能不能进入信息、交战、reset、终局这条组合？



| 指标 | 观察口径 | 影响运营判断 |
|-|-|-|
| Buff 后 pick rate 变化 | 加强前后是否上升 | 判断改动是否被接收 |
| Buff 后 Top 5 / PPG | 上升后是否真的带来收益 | 判断是有效加强还是短期尝鲜 |
| 阵容进入率 | 是否进入 Top 5 主流阵容 | 判断能否融入职业队组合链路 |
| 替代位竞争 | 它要挤掉 Recon、Support、Controller 的哪个槽位 | 判断三人阵容机会成本 |
| 地图限定性 | 是否只在特定地图出现 | 判断是地图专精还是版本趋势 |
| 使用队伍分布 | 是少数队伍专精，还是大范围扩散 | 判断是个人打法还是版本答案 |



以 Mad Maggie 这类破点 / 反掩体角色为例，她的价值不能只看数值有没有加强，而要看她有没有进入职业队真正需要的岗位。

如果当前版本最缺的是稳定信息、控点和 reset，那么 Crypto、Wattson、Gibraltar、Newcastle 的岗位优先级就会更高。Mad Maggie 即使得到加强，也可能因为挤不掉这些关键岗位而无法进入主流。如果 Gibraltar / Newcastle / Rampart 高集中，但 Mad Maggie 仍然没有进入主流阵容，说明问题可能不在于没有反制目标，而在于她的反制成本、阵容机会成本或执行稳定性仍然不够。

## 6.6 普通玩家与职业赛场差异：避免只为职业端调版本

职业赛场是高组织度、高沟通、高执行环境。职业端暴露的问题很有价值，但不能直接等同于普通玩家环境。

因此，实际上需要接入普通端数据，判断职业问题有没有向大众环境扩散。



| 指标 | 我看什么 | 影响运营判断 |
|-|-|-|
| 全段位 pick rate | 普通玩家是否也大量使用 | 判断职业问题是否扩散 |
| 分段 pick / win rate | 不同段位表现差异 | 判断是高组织度专属强度还是大众强度 |
| KDA / 胜率 / 使用率 | 普通环境是否真的强 | 判断是否适合直接数值削弱 |
| 玩家反馈 | 是否觉得难反制、无聊、同质化 | 判断体验问题是否大于强度问题 |
| 职业端 vs 普通端差异 | 职业高 pick、普通低 pick 是否存在 | 判断是否需要职业向规则处理 |
| 赛事观赏性 | 镜像阵容、终局重复、比赛节奏同质化 | 判断是否需要赛事规则介入 |



如果职业端过强但普通端不强，优先处理高组织度协同，而不是直接砍基础数值。如果职业端和普通端都过强，才更适合直接数值削弱。如果强度未必超标，但职业比赛高度重复、观赏性下降，可以考虑赛事规则、地图池或 Ban / Pick 机制介入。

Year 5 引入 Legend Ban 的意义也在这里：它不只是一次赛事规则变化，而是在承认“职业赛场的收敛速度太快，单靠常规平衡未必能维持观赏性和多样性”。



# 7.第四层：从风险标志到运营动作

**因为我无法拿到普通模式或者rank的数据，那么如果暂时不考虑设计师想推广哪个职业、哪个角色或哪把枪，只从 ALGS 赛场平衡出发，版本运营应该怎么判断和行动？**

## 先说结论

职业队不断找到新的最高确定性组合。

- Split 1 是 Bangalore / Bloodhound / Caustic的信息、烟雾、控场组合。
- EWC 是 HAVOC / Hemlok的稳定输出组合。
- Split 2 是 Crypto / Akimbo的新组合。
- Championship 是 Gibraltar / Newcastle的完整闭环。

所以如果只看赛场平衡，版本运营要追踪的不是“谁 pick rate 高”，而是：

**有没有一套选择同时降低失误成本、压缩替代打法，并且让强队可以稳定复制。**

## 第三层指标落地：四次赛事风险标志

我把第三层的指标系统转成一张风险表。这里的“风险等级”不是官方标准，而是作品集里的运营判断口径：当阵容、职业槽位、武器距离和 reset 容错同时异常时，优先级就提高。



| 赛事 | 风险等级 | 关键标志 | 我会采取的运营动作 |
|-|-|-|-|
| Split 1 Playoffs | 高 | Top 1 阵容 53.2%，Bangalore 88.6%，Bloodhound 87.0%，Caustic 57.8% | 进入调优评估，优先拆信息 / 烟雾 / 控场协同 |
| EWC | 高 | Top 1 阵容只有 18.2%，但 AR 击杀占比 67.7%，HAVOC 33.9%，Hemlok 21.1% | 进入武器生态预警，重点看稳定输出核心是否替代旧 meta |
| Split 2 Playoffs | 中到高 | Crypto 71.5%，Mozambique Akimbo 33.2%，Top 3 阵容 65.7% | 监控信息刚需和 Akimbo 强度 |
| Championship | 极高 | Gibraltar 99.8%，Newcastle 95.8%，Support 202.3%，Top 1 阵容 65.7%，Top 3 阵容 91.5%，Shotgun 65.0% | 系统调优 + 赛事规则介入，单点削弱很难解决 |



这张表里最重要的不是哪个数字最大，而是风险形态变了。

Split 1 的问题是旧阵容稳定；EWC 的问题是武器稳定；Split 2 的问题是新机制生效过头；Championship 的问题是职业分工彻底占据生态位置。

## Split 1：不是只削 Bangalore，而是拆信息 / 烟雾 / 控场收益

Split 1 的风险很直接：阵容集中度和角色 pick rate 同时过高。

- `Bangalore, Bloodhound, Caustic` Top 1 阵容覆盖率 53.2%。
- Bangalore pick rate 88.6%。
- Bloodhound pick rate 87.0%。
- Caustic pick rate 57.8%。
- Top 3 阵容覆盖率 70.2%。

如果只看表面，很容易说“Bangalore 太强”。但从赛场平衡角度，我不会先把问题写成 Bangalore 单点强度，而会写成：

**烟雾、扫描、控场、稳定中远距离输出组成了一套低风险推进和终局处理方式。**

判断：

- 这不是普通的高 pick，而是阵容、角色和打法一起集中。
- Bloodhound 让烟雾环境里的信息差更稳定，Caustic 让终局空间更难反制。
- 如果只动 Bangalore，职业队可能继续寻找下一个烟雾或遮蔽环境里的信息优势。

可选调优方向：

- 降低穿烟信息获取的稳定性，让烟雾不再自动绑定扫描角色。
- 给非扫描阵容更多可用的信息入口，避免队伍只能在 Bloodhound 体系里拿确定性。
- 控制 Caustic 这类终局控场收益，重点看它是不是让已经占点的队伍过度安全。
- 武器侧关注 30-30 / Digital Threat 这类能放大中远距离和烟雾收益的组件。

这轮的运营重点不是“打掉某个角色”，而是拆掉一个组合：信息优势 + 遮蔽环境 + 控场终局。

## EWC：阵容分散不代表健康，AR 接管了输出核心

EWC 看起来更健康，因为阵容集中度明显下降：

- Top 1 阵容从 53.2% 降到 18.2%。
- Top 3 阵容从 70.2% 降到 47.7%。

但同一时间，武器生态出现了另一种集中：

- AR 击杀占比 67.7%。
- HAVOC 单武器击杀占比 33.9%。
- Hemlok 单武器击杀占比 21.1%。
- Shotgun 只有 1.4%，SMG 也被压缩。

这说明旧阵容被打散后，职业队没有自然走向多样化，而是迁移到更稳定的武器答案。

运营判断：

- EWC 不适合马上说“版本健康”，因为角色分散掩盖了武器集中。
- HAVOC / Hemlok 不是单纯击杀高，它们共同占据了职业队最稳定的输出距离。
- 近战武器缺少空间，会让圈边推进和强开打法更难获得正反馈。

可选调优方向：

- 先看 HAVOC / Hemlok 的稳定性、后坐力、弹药经济、有效距离和伤害转击杀效率。
- 如果 AR 高伤害但 FWR 普通，可以优先调消耗和经济，而不是直接砍击杀能力。
- 给 Shotgun / SMG 明确的上场场景，避免武器生态只剩“中远距离稳定输出”。
- 调武器时要同时监控替代答案，避免从 AR 集中直接跳到另一把枪集中。

## Split 2：Shockwave 生效了，但 Akimbo 和 Crypto 都需要进入预警

Split 2 的数据比较微妙，因为它既证明了版本改动有效，也暴露了“生效过头”的风险。

有效的一面：

- AR 从 67.7% 降到 33.1%。
- HAVOC 从 33.9% 降到 8.2%。
- Hemlok 从 21.1% 降到 9.5%。

风险的一面：

- Mozambique Akimbo 单武器击杀占比 33.2%。
- Shotgun/Akimbo 类别击杀占比 34.3%。
- Crypto pick rate 71.5%。
- Top 3 阵容覆盖率回升到 65.7%。

这里我不会把 Crypto 和 Mozambique 放在同一种问题里。

Mozambique Akimbo 更像武器规则和数值风险：它突然成为单武器击杀核心，说明爆发窗口、拾取稳定性、有效距离或弹药经济可能过于舒服，比如作为霰弹枪，2组备弹就充足了可以携带其他更多的物品，另外双持的存在，可以考虑在前期单持过渡，比别的枪械多一种过渡方案。

Crypto 更像职业信息刚需：高 pick 不一定说明它伤害超标，而是说明职业队在这个版本里非常需要稳定信息、转移和战术视野。

判断：

- 对 Akimbo，要看它是不是让近战击杀变得过度稳定。
- 对 Crypto，要看没有 Crypto 的阵容是否仍有稳定上分打法。
- 如果 Crypto 高 pick 但 Top 5 / PPG 不极端，不应直接大削，而应补替代信息方案和反制方案。

可选调优方向：

- Mozambique Akimbo：优先检查有效距离、爆发窗口、拾取稳定性和 Hammerpoint 相关收益。
- Crypto：优先增加可反制性，例如 drone 行为反馈、风险暴露、替代 Recon 信息入口。

## Championship：最高风险是 Support / 防守 / reset 体系

Championship 是四次赛事里最需要运营介入的一次。

关键标志非常集中：

- Gibraltar pick rate 99.8%。
- Newcastle pick rate 95.8%。
- Rampart pick rate 69.4%。
- Support 职业槽位 202.3%，约等于平均每队带两个 Support。
- Top 1 阵容覆盖率 65.7%。
- Top 3 阵容覆盖率 91.5%，Top 5 阵容覆盖率 97.4%。
- Shotgun 击杀占比 65.0%。
- 场均 rez 19.4，高于前三次赛事；场均 rspn 3.8，也处在高位。

这里如果只说“Shotgun 太强”，会漏掉真正的问题。

Shotgun 高占比当然需要看，但它不是孤立发生的。Gibraltar Dome、Newcastle Shield、Rampart 掩体和 Support reset 让职业队更容易把战斗拖到近距离、可掩护、可反复救起的空间。于是 Shotgun 变成最合适的收割工具。

运营判断：

- Championship 的问题不是某个点超标，而是系统组合过于稳定，以及初次尝试给予职业体系数值过高。
- 双 Support 降低失败成本，Gibraltar / Newcastle / Rampart 提供安全屋，Shotgun 接管安全屋内的击杀。
- 这套组合同时影响生存、交战距离和终局处理，所以只削一把枪很可能只是换另一把近战武器。

可选调优方向：

- 先降低失败成本，降低Support分工数值：检查 Support 小药收益、救起速度、救起后回血、Mobile Respawn Beacon 获取便利性。
- 再增加反制入口：让 Dome、Mobile Shield、掩体有更清晰的破坏方式或更高使用成本。
- 最后看武器：如果防守重置体系不变，Shotgun 数值调整要谨慎；否则可能误伤普通玩家，却没有解决职业端近战环境。
- 赛事侧可以介入：当 Top 1 / Top 3 / Top 5 阵容同时极高时，Ban / Pick 或地图池调整比常规数值补丁更直接。

这也是我认为 Championship 需要进入“系统调优 + 赛事规则介入”的原因。

## Mad Maggie：无人在意也能说明问题

第三层提到“被加强了还是没人选”的问题，Mad Maggie 是一个很适合放进运营观察组的例子。

在 Year 4 这几次赛事里，她一直没有进入职业主流：

- Split 1：0.16%。
- Split 2：0.94%。
- Championship：0.51%。

从普通理解看，Mad Maggie 是破点、反掩体、强开角色。按理说当 Gibraltar / Newcastle / Rampart 高集中时，她应该有反制价值。但数据说明，至少在 Year 4 的职业赛场里，她没有成为可复制答案。

Mad Maggie 不是 Year 4 中“被加强但失败”的典型案例，而是“反制角色为什么没有进入职业主流”的观察样本。她理论上能反掩体、破点、强开，但如果这个反制收益不足以弥补她不提供稳定信息、控点或 reset 的机会成本，她就很难挤进三人阵容。Year 5 Takeover 让她的 Wrecking Ball 能摧毁 Dome / Mobile Shield，更像是在给这类反制角色补充入场机会。

## Year 5 验证：实际变更也是系统调整 + 赛事规则

Championship 之后的实际更新，和上面的判断方向是吻合的。

第一条线是版本系统。Takeover 版本处理的不是单个 Gibraltar 或 Newcastle，而是整套 Support / 防守 / 反制系统：

- Support 不再拥有小药快速治疗和治疗时加速。
- Crypto EMP 和 Mad Maggie Wrecking Ball 可以摧毁 Gibraltar Dome。
- Mad Maggie 可以摧毁 Newcastle Mobile Shield。
- Assault 职业被重做，获得更直接的战斗和红甲成长价值。
- Arsenals 加入，让队伍更稳定地规划武器和弹药。

这说明官方后续没有简单把 Championship 的问题理解成“Shotgun 太强”或者“Gibraltar 太强”，而是在处理 Support、防守技能、进攻反制和资源规划这些底层系统。

第二条线是赛事规则。ALGS Year 5 引入 Legend Bans：一个 series 里，第一局所有传奇可用，之后会根据使用率禁用传奇，并且有职业类别保护规则，避免某一职业被完全禁空。

这件事对于整个职业赛场影响很大。它不是把 Gibraltar 从 99.8% 调到 80%，而是直接阻止同一套最优阵容无成本复制整个 series。

对职业队来说，这会迫使他们准备第二、第三套阵容；对观众来说，BP 和临场适应会变成内容的一部分；对设计师来说，它也能暴露哪些角色只是被版本压住，哪些角色是真的缺少职业价值。

因此，Year 5 的现实回应可以作为第四层的验证：

**当职业赛场出现系统级收敛时，最合理的运营动作不一定是单点削弱，而是版本系统调整和赛事规则工具一起使用。**

# 8. 数据来源与 AI 使用说明

## 数据来源

- EA 官方 Upheaval Patch Notes：<https://www.ea.com/games/apex-legends/apex-legends/news/upheaval-patch-notes>
- EA 官方 Shockwave Patch Notes：<https://www.ea.com/games/apex-legends/apex-legends/news/shockwave-patch-notes>
- EA 官方 From The Rift Season Updates：[https://www.ea.com/games/apex-legends/apex-legends/news/from-the-rift-season-updates](https://www.ea.com/games/apex-legends/apex-legends/news/from-the-rift-season-updates)
- EA 官方 Takeover Patch Notes：[https://www.ea.com/games/apex-legends/apex-legends/news/takeover-patch-notes](https://www.ea.com/games/apex-legends/apex-legends/news/takeover-patch-notes)
- EA 官方 Year 4 Split 1 Playoffs 说明：<https://algs.ea.com/en/year-4/split-1-2024/news/year-4-split-1-playoffs-eyntk>
- EA 官方 Year 4 Split 2 Playoffs 说明：<https://algs.ea.com/en/year-4/split-2-2024/news/algs-year-4-split-2-playoffs-dates-venue>
- EA 官方 Year 4 Championship 概览：<https://algs.ea.com/en/year-4/champs-2025/competition-overview>
- Apex Legends Status ALGS 数据页：<https://apexlegendsstatus.com/algs/>
- EA 官方 Year 4 Split 2 Pro League / POI Draft 说明：<https://www.ea.com/ea-play/news/y4-s2pl-eyntk>
- EA 官方 Year 5 公告 / Legend Bans 说明：<https://algs.ea.com/en/year-5/algs-open/news/Year5>



## AI 使用说明

本项目使用 AI 辅助完成公开数据整理、代码生成和文本润色。为了避免 AI 误差，我对关键指标进行了人工复核：

1.  抽样检查赛事局数、武器数据与原始页面是否一致； 
2.  重新测算击杀分占比、Top 5 率、阵容集中度三个核心指标； 
3.  对异常值进行回查，例如 Mozambique Akimbo、Gibraltar / Newcastle pick rate、Championship Shotgun 占比。  
 本报告的核心问题设定、指标选择、版本解释和运营建议由本人完成，AI后期文字润色。
