# 科研绘图开放素材检索记录

首批检索日期：2026-11-02；[2026-11-03 的扩展核验与新增来源](EXPANSION-2026-11-03.md) 已另行记录。目标是为论文示意图、课件、海报和实验流程图寻找可以下载、改编及再分发的图形素材，并保存可追溯的来源与许可。

## 检索范围与方法

本次使用公开 GitHub 仓库搜索、上游 README、许可证文件、实际 SVG 文件和配套元数据交叉核对。使用过的检索词包括 `scientific icons`、`biological illustrations`、`Reactome icons`、`Togo picture gallery`、`SciDraw`、`medical illustration svg`、`bioicons`、`science illustration CC0`，并沿已确认项目的参考链接继续查找。通用图标、气象、地理与生态素材另按其上游许可整理。

这是一轮可核实来源的跨领域检索，**不是穷尽全网的清单**。当前运行环境允许访问 GitHub 和部分软件分发网站，但 `smart.servier.com`、`scidraw.io`、`reactome.org` 等站点的直接请求被网络代理拒绝（403）；不能把无法访问写成网站下线，也不能把第三方的许可证描述当成已完成官网核验。未取得可核实再分发依据的独立站素材只列链接，不批量镜像。

## 已核实的生物医学素材来源

| 来源 | 科研用途与素材范围 | 实际核验的许可依据 | 下载与整理要点 |
| --- | --- | --- | --- |
| [Bioicons](https://github.com/duerrsimon/bioicons) | 生物、化学、医学、实验器材等 SVG；包含多个作者和来源 | [README 的 Credits](https://github.com/duerrsimon/bioicons#credits) 明确要求引用每个图标及其各自许可证 | 以图标元数据为准；不能把整库统一改成 MIT 或 CC0。原图、作者、许可版本和来源一起保存。 |
| [Reactome Illustrations](https://github.com/reactome/reactome_illustrations) | 蛋白质、化合物、受体、转运体、细胞、组织等精细图标 | [固定版本 LICENSE](https://github.com/reactome/reactome_illustrations/blob/9b70b1d706086d3d917f4150ab59aa65815b3c47/LICENSE)：Apache-2.0；逐一扫描当前 `icons/` 的 SVG/XML 未发现另列许可证 | 固定版本 `9b70b1d706086d3d917f4150ab59aa65815b3c47` 的 `icons/` 有 2,571 个 SVG 和 2,571 个配套 XML，合计约 34.6 MB。XML 包含名称、分类、描述、设计师、审校人和数据库引用，须保留。直接下载已提交文件无需 Figma token。 |
| [EMBL-EBI Icon Fonts](https://github.com/ebiwd/EBI-Icon-fonts) | 模式生物轮廓、生物学概念、化学反应方向 | [固定版本 LICENSE.md](https://github.com/ebiwd/EBI-Icon-fonts/blob/f3d2154e26091041f20828b60126254e93eccabe/LICENSE.md)：SVG/PNG 为 CC BY-SA 4.0，代码为 Apache-2.0；捆绑第三方素材另行授权 | 仅选 `source/species`（66 个）、`source/conceptual`（10 个）、`source/chemistry`（4 个），共 80 个 SVG；不混入 common、social 和商标素材。文件名就是可读标识，无须安装字体或从 Unicode 字符猜名称。 |
| [ID & Immunology Icons](https://github.com/apsmunro/bioicons-id) | 病原体、免疫细胞、药物、耐药、临床和感染传播；彩色与单色版本 | [固定版本 README](https://github.com/apsmunro/bioicons-id/blob/412d108120ef023c4a5049e103e91a858c5ab7ed/README.md) 与 [LICENSE](https://github.com/apsmunro/bioicons-id/blob/412d108120ef023c4a5049e103e91a858c5ab7ed/LICENSE) 明确声明 CC0 1.0 | `catalogue.json` 有 163 条主图记录，含名称、分类、描述、标签、彩色与单色路径；`icons/` 共 347 个 SVG，另含肤色变体。按原始分类和文件路径保留。 |

Reactome 的 `ehld/` 和 `statics/` 是整幅通路图，通常带背景、文字、数据库标识和复杂结构。本次优先整理可组合的 `icons/`；未把整幅通路图伪装成单个图标。其分类标签允许一图多类，分类计数不能直接相加视为文件数。

## 继续查找的独立站与专题资源

以下链接用于拓展素材来源；除已经从 Bioicons 取得并保留原有许可的图形外，**列出链接不表示本仓库已镜像该站全部素材或确认全站统一许可**。

| 资源 | 用途 | 收录边界与下一步 |
| --- | --- | --- |
| [Servier Medical Art](https://smart.servier.com/) | 解剖、生理、疾病、医学示意图 | 用户给出的 CC BY 3.0 对应大量历史素材；Bioicons 明确记录的 Servier 图标按其 CC BY 3.0 元数据保留。不能据此推定官网当前所有新素材同为 3.0。官网当前条款、下载方式和自动抓取限制需在可访问时直接核验。 |
| [SciDraw](https://scidraw.io/) | 科研手绘图、动物实验、神经科学与实验装置 | 需读取每件作品的作者和实际许可证后再收录；当前站点直接访问受限，未批量下载。 |
| [DBCLS Togo Picture Gallery](https://togotv.dbcls.jp/en/pics.html) | 分子生物学、实验技术与生命科学插画 | Bioicons README 将其列为素材来源之一；从 Bioicons 获得的图形保留各自作者和许可。独立站新增作品仍须逐件核验。 |
| [NIH / NIAID BioArt Source](https://bioart.niaid.nih.gov/) | 公共卫生、细胞、病原体、实验设备与医学插画 | 不把所有 NIH 网站图片一概认定为公有领域：需区分政府作品、承包作者和第三方素材，逐件核验使用条款。 |
| [PhyloPic](https://www.phylopic.org/) | 动植物、化石和分类群轮廓 | 作品许可可能不同。优先考虑 CC0、CC BY、CC BY-SA；带 NC 或 ND 的图片不进入本仓库开放再分发集合。需保留作者与分类群信息。 |
| [IAN Image Library](https://ian.umces.edu/media-library/) | 生态、环境、湿地、水文与资源管理示意图 | 候选生态专题库。须核验具体图片和当前许可条件后下载；本记录不把旧文章的许可摘要当作当前站点整体授权。 |
| [Wikimedia Commons](https://commons.wikimedia.org/) | 学科覆盖广的示意图、物种图片、地学与器材 | 每个文件页有独立许可和作者；仅对具体文件授权，不能给整站图片贴统一开放许可证。 |
| [OpenClipart](https://openclipart.org/) | 通用矢量插画及部分科学器材 | 作为补充候选；收录前检查上传者、作品来源和是否存在第三方标识，不将其与有明确作者链条的科学插画等同。 |

商业订阅图库的可预览图片、仅允许在论文中使用而禁止再分发的素材、没有明确许可的 GitHub 图片目录，都不会仅凭“免费”“公开可看”或“科研用途”下载后重新发布。

## 署名与复用

- CC0：无需强制署名；仍保留来源，方便科研追溯。
- CC BY：引用作者、素材名称或标识、来源链接、许可名称与链接；如有改动应注明。
- CC BY-SA：在 CC BY 要求之外，发布改编图形时遵守相同方式共享条款；不能把这些图形重新标成 MIT。
- Apache-2.0 / MIT：保留相应许可证和上游版权声明；Apache 素材如有上游 NOTICE 也须保留，修改文件时注明。
- 混合许可库：逐文件许可优先于网站代码的许可证；科研内容是否准确仍需作者自行核验。

建议论文致谢格式：`图中 [素材名称] 取自 [作者 / 素材库]（[来源 URL]），依据 [许可证及 URL] 使用；[未改动 / 说明修改内容]。` 最终以所用图形附带的许可和元数据为准。
