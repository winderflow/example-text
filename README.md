# 科研绘图开放素材库

为论文示意图、实验流程图、科研海报和课件整理的开放 SVG 素材库。已实际下载 **11,846 个 SVG 文件，来自 14 个上游仓库，分为七大学科，原始 SVG 合计约 364.6 MB**。彩色、单色、线框等独立样式分别计数，数量不等于独立科学概念数。

检索与下载日期：2026-11-02。素材原始字节保持不变，逐图保存作者、许可证、固定版本来源及 SHA-256。**本库没有统一的素材许可证**；详见 [许可与署名指南](docs/LICENSES.md)。

## 浏览与下载

- 打开 [在线图库（Pages 启用后可用）](https://winderflow.github.io/example-text/)，按学科、素材库、许可证和中英文关键词筛选；点击卡片可下载原始 SVG、查看来源和复制署名。
- 直接在下方分类目录下载单图；批量获取可使用 GitHub 的 **Code → Download ZIP** 或 `git clone https://github.com/winderflow/example-text.git`。
- 全量目录与逐图署名：[manifest.csv](data/manifest.csv)（可用 Excel 打开）、[catalog.json](data/catalog.json)。下载 SVG 时同时保留对应的署名和许可记录。
- SVG 可导入 Inkscape、Illustrator、PowerPoint 等软件；电路符号库为一张整图，可在矢量编辑器中选取元件。SVG 不是位图照片库。

| 学科分类 | SVG 文件数 |
| --- | ---: |
| [生物医学](assets/biomedical/) | 6,513 |
| [化学与分子](assets/chemistry/) | 654 |
| [生态与物种](assets/ecology/) | 927 |
| [地理、气象与空间](assets/earth-space/) | 1,973 |
| [工程与物理](assets/engineering/) | 520 |
| [计算与数据流程](assets/computing/) | 1,092 |
| [科研交流与通用](assets/general/) | 167 |

## 已下载来源

| 素材库 | SVG 文件数 | 许可概览 | 收录范围 |
| --- | ---: | --- | --- |
| [Bioicons（含 Servier / Togo）](https://github.com/duerrsimon/bioicons) | 2,601 | 逐图授权 | 生物、医学、植物、实验器材；含经 Bioicons 分发的 Servier 与 DBCLS 素材，保留其历史逐图许可。 |
| [ID & Immunology Icons](https://github.com/apsmunro/bioicons-id) | 347 | CC0-1.0 | 病原体、免疫细胞、器官与感染传播，含彩色和单色版本。 |
| [Reactome Illustrations](https://github.com/reactome/reactome_illustrations) | 2,257 | Apache-2.0 | Reactome 官方蛋白、化合物、细胞、组织和通路组件；保留原始 XML 元数据。 |
| [EMBL-EBI Science Icons](https://github.com/ebiwd/EBI-Icon-fonts) | 80 | CC-BY-SA-4.0 | 仅选 chemistry、conceptual、species 科学符号，不含第三方品牌和通用字库。 |
| [Health Icons](https://github.com/resolvetosavelives/healthicons) | 2,128 | CC0-1.0 | 公共卫生、症状、医疗设备、人体与医疗服务图标，保留上游样式。 |
| [OpenMoji 科研选集](https://github.com/hfg-gmuend/openmoji) | 419 | CC-BY-SA-4.0 | 动物、植物、地理天气、科学与技术主题彩色符号；逐图作者信息。 |
| [Maki](https://github.com/mapbox/maki) | 215 | CC0-1.0 | 地图兴趣点、自然环境、基础设施图标。 |
| [Temaki](https://github.com/ideditor/temaki) | 557 | CC0-1.0 | 地理生态、交通、基础设施、土地利用地图符号。 |
| [Meteocons / Weather Icons](https://github.com/basmilius/weather-icons) | 708 | MIT | 天气、风力、降水与天体符号，静态 fill / line / monochrome 三款。 |
| [Game Icons 科研选集](https://github.com/game-icons/icons) | 721 | 逐图授权 | 从作者目录按公开关键词选取自然、生物、化学、物理和工程图标。 |
| [Tabler 科研与流程图选集](https://github.com/tabler/tabler-icons) | 1,754 | MIT | 科学、设备、网络、数据处理与流程图符号，outline / filled 样式。 |
| [Equinor Engineering Symbols](https://github.com/equinor/engineering-symbols) | 55 | MIT | 工业过程与工程设备的标准化 SVG 符号，保留原始编号。 |
| [Inkscape Circuit Symbols](https://github.com/keikawa/InkscapeCircuitSymbols) | 1 | MIT | 整张电路符号 SVG 图板；在 Inkscape 内打开后选取所需元件。 |
| [Scienceicons 开放科学选集](https://github.com/continuous-foundation/scienceicons) | 3 | MIT | 开放获取及科研交流基础符号；不收录第三方品牌。 |

Bioicons 子集中含 **1,374 个署名 Servier**、**473 个署名 DBCLS** 的文件；这是通过 Bioicons 取得的具体历史素材，不是对 Servier / Togo 当前官网的全站镜像或完整性声明。上游原始说明、完整许可及元数据见 [licenses/](licenses/)。

部分来源只选择科研相关主题：不把全站通用、娱乐或品牌图标计为全库下载。Reactome 遵循上游 `skip=true` 标记；不收录解析失败、活动内容或依赖外部资源的 SVG。具体排除文件和原因见 [excluded.json](data/excluded.json)；它只记录候选集的技术及明确许可筛选，不枚举所有未选中的主题。

## 更多资源与检索边界

[检索记录](docs/RESEARCH.md) 列出 SciDraw、PhyloPic、IAN、NIH BioArt、Wikimedia Commons 等继续检索入口；[扩展库清单](docs/LICENSES.md#更多已核实许可的官方资源仅链接未在本次下载) 另含 Lucide、Font Awesome、Material Icons、Bootstrap、IconPark 和 Simple Icons。这些**仅列链接的资源未下载，不计入上述数量**。

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

重建不自动跟随上游最新版本。修改锁文件前应重新核实许可和导入范围；构建器拒绝脏的上游工作区，并只移除上次清单管理且未被用户修改的旧素材。`dist/` 是可直接部署的静态站点。

## GitHub Pages 部署

仓库提供 [.github/workflows/pages.yml](.github/workflows/pages.yml)：向 `main` 推送时自动校验并部署，亦可在 Actions 手动运行。首次使用需在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**，再运行 **Validate and deploy research gallery**。是否已上线以 Actions 的部署成功记录及实际站点响应为准；提交工作流不等于已完成线上部署。

站点地址：`https://winderflow.github.io/example-text/`。若 GitHub 套餐或仓库可见性不支持 Pages，仓库内的原图和本地页面仍可使用。

## 许可

本项目自行编写的网页和脚本采用 [MIT](LICENSE)。`assets/`、`licenses/` 内的第三方文件保持原始许可，**不受本站代码 MIT 许可重新授权**。CC BY / CC BY-SA 素材使用时需要署名，SA 素材发布改编作品时还有相同方式共享要求；参见 [许可指南](docs/LICENSES.md)。
