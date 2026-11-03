# 科研绘图开放素材库

为论文示意图、实验流程图、科研海报和课件整理的开放素材库。现有 **16,452 张原始图片，来自25个上游仓库**：16,335个SVG和117张原生高清JPEG。另保留418张长边2400像素的PNG兼容版本，以及72图、20页的PowerPoint素材板；格式转换不重复计为新图片。

首批检索：2026-11-02；PPT质量整理：2026-11-03；本轮新图扩展：2026-11-04。素材原始字节保持不变，逐图保存作者、许可证、固定版本来源及 SHA-256。**本库没有统一的素材许可证**；详见 [许可与署名指南](docs/LICENSES.md)。

## 浏览与下载

- **[本轮新增316张科研图片：按图名直接下载](docs/NEW-OPEN-ART-2026-11-04.md)**，包括117张原生高清解剖图、164张完整生物通路图和35张实验室原创图形。

- **[直接下载 PowerPoint 素材板](downloads/ppt-illustrations.pptx)**：72 张图片可逐张复制，每页备注保留完整署名。GitHub 文件页可点击 Download raw 下载。
- **[按名称和学科查找高清 PNG](docs/PPT-INDEX.md)**：418 张原图的2400像素兼容版本；[PPT 使用指南](docs/PPT-GUIDE.md)。
- 在图库的“文件格式”中选择“PPT 高清 PNG”或“高清原图 PNG/JPG”，可按学科查找并查看实际像素尺寸。

- 打开 [在线图库（Pages 启用后可用）](https://winderflow.github.io/example-text/)，按学科、素材库、许可证和中英文关键词筛选；点击卡片可下载原始 SVG、查看来源和复制署名。
- 直接在下方分类目录下载单图；批量获取可使用 GitHub 的 **Code → Download ZIP** 或 `git clone https://github.com/winderflow/example-text.git`。
- 全量目录与逐图署名：[manifest.csv](data/manifest.csv)（可用 Excel 打开）、[catalog.json](data/catalog.json)。下载 SVG 时同时保留对应的署名和许可记录。
- SVG 可导入 Inkscape、Illustrator、PowerPoint 等软件；电路符号库为一张整图，可在矢量编辑器中选取元件。SVG 不是位图照片库。

| 学科分类 | 原图文件数 |
| --- | ---: |
| [生物医学](assets/biomedical/) | 7,319 |
| [化学与分子](assets/chemistry/) | 684 |
| [生态与物种](assets/ecology/) | 1,062 |
| [地理、气象与空间](assets/earth-space/) | 3,379 |
| [工程与物理](assets/engineering/) | 1,061 |
| [计算与数据流程](assets/computing/) | 2,509 |
| [科研交流与通用](assets/general/) | 438 |

## 已下载来源

| 素材库 | 类型 | 原图文件数 | 许可概览 | 收录范围 |
| --- | --- | ---: | --- | --- |
| [Bioicons（含 Servier / Togo）](https://github.com/duerrsimon/bioicons) | 科研专题 | 2,819 | 逐图授权 | 生物、医学、植物、实验器材；含经 Bioicons 分发的 Servier 与 DBCLS 素材，保留其历史逐图许可。 |
| [ID & Immunology Icons](https://github.com/apsmunro/bioicons-id) | 科研专题 | 347 | CC0-1.0 | 病原体、免疫细胞、器官与感染传播，含彩色和单色版本。 |
| [Reactome Illustrations](https://github.com/reactome/reactome_illustrations) | 科研专题 | 2,421 | Apache-2.0 | Reactome 官方蛋白、细胞、组织和通路组件，以及完整生物通路插画；图标保留原始 XML 元数据。 |
| [EMBL-EBI Science Icons](https://github.com/ebiwd/EBI-Icon-fonts) | 科研专题 | 80 | CC-BY-SA-4.0 | 仅选 chemistry、conceptual、species 科学符号，不含第三方品牌和通用字库。 |
| [Health Icons](https://github.com/resolvetosavelives/healthicons) | 科研专题 | 2,128 | CC0-1.0 | 公共卫生、症状、医疗设备、人体与医疗服务图标，保留上游样式。 |
| [OpenMoji 科研选集](https://github.com/hfg-gmuend/openmoji) | 通用绘图符号 | 419 | CC-BY-SA-4.0 | 动物、植物、地理天气、科学与技术主题彩色符号；逐图作者信息。 |
| [Maki](https://github.com/mapbox/maki) | 科研专题 | 215 | CC0-1.0 | 地图兴趣点、自然环境、基础设施图标。 |
| [Temaki](https://github.com/ideditor/temaki) | 科研专题 | 557 | CC0-1.0 | 地理生态、交通、基础设施、土地利用地图符号。 |
| [Meteocons / Weather Icons](https://github.com/basmilius/weather-icons) | 科研专题 | 708 | MIT | 天气、风力、降水与天体符号，静态 fill / line / monochrome 三款。 |
| [Game Icons 科研选集](https://github.com/game-icons/icons) | 通用绘图符号 | 721 | 逐图授权 | 从作者目录按公开关键词选取自然、生物、化学、物理和工程图标。 |
| [Tabler 科研与流程图选集](https://github.com/tabler/tabler-icons) | 通用绘图符号 | 1,754 | MIT | 科学、设备、网络、数据处理与流程图符号，outline / filled 样式。 |
| [Equinor Engineering Symbols](https://github.com/equinor/engineering-symbols) | 科研专题 | 55 | MIT | 工业过程与工程设备的标准化 SVG 符号，保留原始编号。 |
| [Inkscape Circuit Symbols](https://github.com/keikawa/InkscapeCircuitSymbols) | 科研专题 | 1 | MIT | 整张电路符号 SVG 图板；在 Inkscape 内打开后选取所需元件。 |
| [Scienceicons 开放科学选集](https://github.com/continuous-foundation/scienceicons) | 通用绘图符号 | 3 | MIT | 开放获取及科研交流基础符号；不收录第三方品牌。 |
| [Lucide 科研符号选集](https://github.com/lucide-icons/lucide) | 通用绘图符号 | 659 | ISC / MIT | 科研仪器、医学、生态、计算与流程符号；继承 Feather 的图标保留 MIT 条件。 |
| [Font Awesome Free 科研选集](https://github.com/FortAwesome/Font-Awesome) | 通用绘图符号 | 447 | CC-BY-4.0 | 选择非品牌的科学、仪器、医学、工程与数据图标；排除同名别名重复文件。 |
| [Bootstrap 科研符号选集](https://github.com/twbs/icons) | 通用绘图符号 | 573 | MIT | 实验、医疗、环境、计算设备、数据和流程符号。 |
| [IconPark 科研与工程选集](https://github.com/bytedance/IconPark) | 通用绘图符号 | 1,015 | Apache-2.0 | 包含上游中文名称、作者和标签的医学、动植物、能源、工业、测量、硬件与数据符号。 |
| [Carbon 科研与工业插图选集](https://github.com/carbon-design-system/carbon) | 通用绘图符号 | 348 | Apache-2.0 | IBM Carbon 的科学、气候、工业、设备和数据概念插图；排除品牌标识。 |
| [Electrical Symbol Library](https://github.com/basverdoes/ElectricalSymbolLibrary) | 科研专题 | 74 | CC0-1.0 | 仅收 src/symbols 独立电气符号；其余文件的非商业许可不用于这些单图。 |
| [Electricalsymbols 工业电气符号](https://github.com/chille/electricalsymbols) | 科研专题 | 32 | CC-BY-SA-3.0 | IEC 工业电气元件、开关、保护、传感器和电机；排除空白文档模板。 |
| [FGDC Geologic Patterns](https://github.com/davenquinn/geologic-patterns) | 科研专题 | 471 | CC0-1.0 | USGS / FGDC 地质、岩性、冰川和地层剖面填充图案；可用于地学论文制图。 |
| [GISsymbology 专题地图符号](https://github.com/GISsymbology/symbols) | 科研专题 | 453 | CC-BY-SA-4.0 | 选取地震微区划、地质图、FGDC 地质符号和水利防护四个许可明确的子库。 |
| [OpenStax 人体解剖与生理历史开放插画](https://github.com/openstax/osbooks-anatomy-physiology) | 科研专题 | 117 | CC-BY-4.0 | 只收录固定历史 CC BY 4.0 版本中逐图核验的高清人体解剖与生理插画；不套用当前非商业版本许可。 |
| [JustFig 原创科研图形](https://github.com/BooneAndrewsLab/justfig-icons) | 科研专题 | 35 | CC0-1.0 | 仅收原创 house 集合中的实验室、细胞、蛋白、免疫和微生物图形，不收聚合库其他来源。 |

Bioicons 子集中含 **1,374 个署名 Servier**、**630 个署名 DBCLS** 的文件；这是通过 Bioicons 取得的具体历史素材，不是对 Servier / Togo 当前官网的全站镜像或完整性声明。上游原始说明、完整许可及元数据见 [licenses/](licenses/)。

部分来源只选择科研相关主题：不把全站通用、娱乐或品牌图标计为全库下载。Reactome 遵循上游 `skip=true` 标记；不收录解析失败、活动脚本或依赖缺失外部图片的 SVG；只允许经逐图哈希核验的静态HTML标签及普通署名链接。具体排除文件和原因见 [excluded.json](data/excluded.json)；它只记录候选集的技术及明确许可筛选，不枚举所有未选中的主题。

## 2026-11-03 扩展

在首批 14 库、11,846 个 SVG 的基础上，本轮实际增加 **9 个来源、4,072 个 SVG**。其中四个是电气、地质和 GIS 科研专题库，五个提供科学、工业及数据流程绘图符号；网页的来源卡片也会标明两类用途。未把单纯字体、缺少图片许可或许可版本冲突的候选凑入已下载数量。

完整的新增范围、许可与排除依据见 [本轮扩展记录](docs/EXPANSION-2026-11-03.md)。

## 2026-11-03 科研插画与 PPT 质量整理

本轮不继续用通用图标增加来源数，而是按用户指定的 Bioicons / Servier / Togo / Wellcome / Commons / RCSB 方向整理：

- 从原有 Bioicons 固定版本恢复 **218 张**此前被兼容性检查误排的原始 SVG，其中包含 **30 张 SwissBioPics**、**157 张 DBCLS** 图形。原始字节、作者和历史许可证保持不变，不计作另一个新图库。
- 为恢复的218张和另外200张专题精选图（181张Servier、19张DBCLS）制作长边2400像素 PNG，共418张。SVG含静态HTML排版时使用PNG预览及PPT兼容版本，避免文字丢失。
- 提供72张图片的PPTX素材板；图片独立可复制，逐图来源与许可放在对应页备注中。`data/ppt-deck.json` 和 `data/ppt-renders.json` 记录素材及导出校验值。
- Wellcome、Wikimedia Commons、RCSB以及Servier/Togo官网的新原件仍被当前云环境网络策略以403阻塞；这些尚未下载的图片不计入任何数量。官方GitHub可取得的Bioicons原图已实际处理。

访问范围、恢复依据和后续官方接口见 [质量核验记录](docs/QUALITY-SOURCES-2026-11-03.md)、[Wellcome / Commons 说明](docs/WELLCOME-COMMONS-NOTES.md)、[RCSB 说明](docs/RCSB-SOURCE-NOTES.md)。所需公开站点与图片接口已保存至云环境网络配置草稿；保存草稿不会立即更新当前运行机器。

## 2026-11-04 新增开放科研原图

本轮新增316张原图：OpenStax历史CC BY4版本的117张高清解剖与生理JPEG、Reactome164张完整通路SVG、JustFig35张原创科研SVG。现有原图16,452张，来源25个；原生JPEG按实际像素尺寸展示，不称为可编辑矢量。

[新增图片下载索引](docs/NEW-OPEN-ART-2026-11-04.md) 提供预览、名称、专题、尺寸和逐图下载。OpenStax当前非商业版本没有混入本库，历史授权证据与章节图注保存在 `licenses/openstax-anatomy/`。原有418张PNG及PPT文件保持不变。

## 更多资源与检索边界

[检索记录](docs/RESEARCH.md) 列出 SciDraw、PhyloPic、IAN、NIH BioArt、Wikimedia Commons 等继续检索入口；[扩展库清单](docs/LICENSES.md#其他官方资源及收录状态) 仍列出 Material Icons 和 Simple Icons 等未导入来源。Lucide、Font Awesome、Bootstrap 和 IconPark 已在本轮从链接清单转为实际入库，具体范围见上表；**仅列链接的来源不计入下载数量**。

本次采用公开仓库搜索、官方 README 与许可证核验，并沿引用链查找来源，覆盖生物医学、化学、生态、地学、物理工程和数据流程；不能保证穷尽全网。部分独立官网受运行环境网络限制，未取得可核实再分发依据的素材未镜像。后续新增时应继续逐件核对许可与作者。

## 本地使用与校验

成品页面已经包含在仓库内，无需 Node 依赖、编译或外部 CDN。使用现有 checkout；云任务已经隔离，除非明确需要，不必额外创建 worktree。

```bash
cd /workspace/example-text
python3 scripts/validate.py
python3 -m http.server 8000
```

在浏览器通过本地 HTTP 打开页面（直接双击 HTML 时浏览器可能禁止读取 JSON）。`validate.py` 验证全部文件的存在性、哈希、XML 格式、许可/作者覆盖、来源提交、Reactome 元数据及 CSV/JSON 数量一致性。

可选的真实浏览器验收需要 Node.js：`npm ci`、`npx playwright install chromium`、`npm run test:browser`。它检查全部来源的抽样渲染、中英文检索、筛选、分页、署名、原图下载哈希和移动布局；不影响无依赖的页面使用。

## 固定版本重建

上游仓库与精确 commit 锁在 [sources.lock.json](data/sources.lock.json)。下载器只获取文件，不运行上游代码，不关闭 TLS 验证；需要 Git、Python 3.10+ 及 GitHub HTTPS 网络访问。完整下载比使用仓库内成品耗时和占盘更多。

```bash
python3 scripts/fetch_sources.py --dest .cache/sources
python3 scripts/build_catalog.py --sources .cache/sources
python3 scripts/validate.py
python3 scripts/build_site.py
```

只需下载单个上游包时可用 `python3 scripts/fetch_sources.py --only carbon-pictograms`；`sparse_paths` 会限制大型单仓库实际检出的目录，已验证固定提交的独立下载。

只重建本轮来源时可用 `python3 scripts/build_catalog.py --sources .cache/sources --only reactome openstax-anatomy justfig-icons`，其余已验证原图会保留。

重建不自动跟随上游最新版本。修改锁文件前应重新核实许可和导入范围；构建器拒绝脏的上游工作区，并只移除上次清单管理且未被用户修改的旧素材。`dist/` 是可直接部署的静态站点。

## GitHub Pages 部署

仓库提供 [.github/workflows/pages.yml](.github/workflows/pages.yml)：普通推送只校验素材、PNG、PPTX 和脚本，不要求启用 Pages。需要网站时，先在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**，再手动运行 **Validate gallery (Pages optional)** 并勾选 `deploy_pages`。是否已上线以部署成功记录及实际站点响应为准；校验成功不等于网页已发布。

站点地址：`https://winderflow.github.io/example-text/`。若 GitHub 套餐或仓库可见性不支持 Pages，仓库内的原图和本地页面仍可使用。

## 许可

高清 PNG 与 PPT 素材板的图像继续采用各自原许可；PPT备注与清单保留逐图署名，合集不替代对原作者的引用。

本项目自行编写的网页和脚本采用 [MIT](LICENSE)。`assets/`、`licenses/` 内的第三方文件保持原始许可，**不受本站代码 MIT 许可重新授权**。CC BY / CC BY-SA 素材使用时需要署名，SA 素材发布改编作品时还有相同方式共享要求；参见 [许可指南](docs/LICENSES.md)。
