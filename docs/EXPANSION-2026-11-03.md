# 专题素材扩展核验（2026-11-03）

本轮优先补充具有学科用途的独立来源，重点为电路绘图、地质填充纹理、地质制图、水文工程和地震微区划。以下数量为固定提交中的原始候选文件数；实际入库还要通过 SVG 格式、外部引用和活动内容检查，以 `data/catalog.json` 为准。

## 实际合并结果

相较首批 14 个来源、11,846 个 SVG，本轮新增 **9 个来源、4,072 个 SVG**，合集达到 **23 个来源、15,918 个 SVG**。新增文件保留原始字节、逐图作者、固定提交、许可版本和 SHA-256；同一图标的样式版本分别计数。

| 本轮来源 | 类型 | 实际新增 SVG |
| --- | --- | ---: |
| [Lucide 科研符号选集](https://github.com/lucide-icons/lucide/tree/e5e55d2b65259c3f2abc5314d0b2c708dbdf2e60) | 通用绘图符号 | 659 |
| [Font Awesome Free 科研选集](https://github.com/FortAwesome/Font-Awesome/tree/14c65a3747d0f3b751f15831fc719236aea8729d) | 通用绘图符号 | 447 |
| [Bootstrap 科研符号选集](https://github.com/twbs/icons/tree/829d2bc2b87543c7d781c815ca4f0feee8cf9e45) | 通用绘图符号 | 573 |
| [IconPark 科研与工程选集](https://github.com/bytedance/IconPark/tree/8dc132da4c85671ba6a5962c87aa2bdafbf158e9) | 通用绘图符号 | 1,015 |
| [Carbon 科研与工业插图选集](https://github.com/carbon-design-system/carbon/tree/31cfe4b5078ad7b4098c31619010c89afed238ab) | 通用绘图符号 | 348 |
| [Electrical Symbol Library](https://github.com/basverdoes/ElectricalSymbolLibrary/tree/ed1c2a3a910969b6de2483249515cce10cfd0a07) | 科研专题 | 74 |
| [Electricalsymbols 工业电气符号](https://github.com/chille/electricalsymbols/tree/bf642743e93551d6aed23e0e05973d54863f4c09) | 科研专题 | 32 |
| [FGDC Geologic Patterns](https://github.com/davenquinn/geologic-patterns/tree/7fdb820b024395f140bd6edb60c99f6001458364) | 科研专题 | 471 |
| [GISsymbology 专题地图符号](https://github.com/GISsymbology/symbols/tree/a20b94a2c284a5bdcd896e13db3e2f9a8115335b) | 科研专题 | 453 |

## 新核实的四个专题库

| 来源与固定版本 | 候选素材范围 | 许可依据 | 整理要点 |
| --- | --- | --- | --- |
| [Electrical Symbol Library](https://github.com/basverdoes/ElectricalSymbolLibrary/tree/ed1c2a3a910969b6de2483249515cce10cfd0a07) | `src/symbols/**/*.svg`，74 个，含 IEC / ANSI 模拟及数字电路元件 | [README 的 License 段](https://github.com/basverdoes/ElectricalSymbolLibrary/blob/ed1c2a3a910969b6de2483249515cce10cfd0a07/README.md#license) 明确只将独立符号按 CC0 1.0 发布；抽查 SVG 内也声明 CC0 | basverdoes 为整理者；应优先保留 SVG RDF 内的原作者和贡献者信息，抽查为 Filip Dominec and contributors。只导入 `src/symbols/`，不将整张库图、示例和说明套上 CC0；仓库其余文件是 CC BY-NC-SA 4.0。许可说明需保留这一范围差异。 |
| [Electricalsymbols](https://github.com/chille/electricalsymbols/tree/bf642743e93551d6aed23e0e05973d54863f4c09) | `Symbols/*.svg`，33 个，含电机、变压器、继电器、开关、接地和接近传感器 | [README 的 Copyright and licensing 段](https://github.com/chille/electricalsymbols/blob/bf642743e93551d6aed23e0e05973d54863f4c09/README.md#copyright-and-licensing) 明确全库 CC BY-SA 3.0 | 作者为 Christian Antila（2017）。保留版本 3.0，不因其他库使用 4.0 而改写。该库以兼容 IEC 60617 为目标，不代表官方标准认证。 |
| [FGDC Geologic Patterns](https://github.com/davenquinn/geologic-patterns/tree/7fdb820b024395f140bd6edb60c99f6001458364) | `assets/svg/*.svg`，471 个，含地表、沉积、火成、变质、冰川及岩性图案的不同配色版本 | [LICENSE](https://github.com/davenquinn/geologic-patterns/blob/7fdb820b024395f140bd6edb60c99f6001458364/LICENSE)：美国政府原始符号属公有领域，本次重制另外按 CC0 发布 | 归属记录为 Daven Quinn / USGS FGDC。保留原始编号与配色后缀；`docs/data.yaml` 说明编号系列。不同配色是多个文件，不应宣称为多个独立地质概念。排除 `docs/fonts/symbol-font.svg`，它是网站图标字体。 |
| [GISsymbology Symbols](https://github.com/GISsymbology/symbols/tree/a20b94a2c284a5bdcd896e13db3e2f9a8115335b) | `collections/{microzonazione,carg,fdgc,sicod}/svg/**/*.svg`，分别 69、110、268、6 个，合计 453 个 | 四个所选目录的各自 `license` 文件都明确链接 CC BY-SA 4.0；[metadata.ini](https://github.com/GISsymbology/symbols/blob/a20b94a2c284a5bdcd896e13db3e2f9a8115335b/metadata.ini) 提供作者与用途 | microzonazione / sicod 署名 Luca Lanteri per Arpa Piemonte；carg / fdgc 署名 Mauro de Donatis per Arpa Piemonte。目录拼写 `fdgc` 按上游原样保留。不是全库统一许可，见下文排除项。 |

FGDC 图案是具有 `viewBox` 和可见路径的独立 SVG，不是仅包含 `<defs>` 的模板。已用 Chromium 抽查 `101-C.svg`：解码成功并显示点状地质纹理，可作为地层柱状图和地质图的纹理样片；如何组合及比例仍需符合绘图目的和具体制图规范。

## 五个科学及工作流符号来源

这些是可用于科研图示的通用矢量符号或概念插图，不能等同于专业解剖、化学结构或物种插图库；网站以“通用绘图符号”标明。按科研相关名称、上游分类和公开的选择规则导入，不将整个网站的所有图标算作科研素材。

| 来源 | 许可与作者依据 | 实际导入规则 |
| --- | --- | --- |
| Lucide | 完整 `LICENSE` 含 ISC 以及从 Cole Bemis / Feather 继承的 MIT；逐图 JSON 有贡献者、分类、标签和历史别名 | `icons/*.svg` 的科研、自然、天气、医学、数学与流程选集；检查当前名称及 `aliases[].name` 是否属于 Feather，保留 `ISC AND MIT` 的双重条件，不因重命名漏标 MIT。 |
| Font Awesome Free | `LICENSE.txt` 明确 SVG 图标为 CC BY 4.0，署名 Fonticons, Inc.；字体与代码许可不套用于图形 | 仅 `svgs/{solid,regular}`；文件名须为 `metadata/icons.json` 的 canonical key，按科研名称筛选，排除 brands、文件别名及重复目录；复制原 SVG，保留其内嵌版权注释。 |
| Bootstrap Icons | 根目录 MIT 及 The Bootstrap Authors 版权声明 | `icons/*.svg` 按科研及流程图关键词筛选，保存原始文件和许可。 |
| IconPark | 根目录 Apache-2.0；`source/icons.json` 给出中文作者、名称、类别和标签 | 选择 Health、Animals、Energy、Industry、Measurement、Weather、Hardware、Charts、Datas、Connect、Components、Graphics、Arrows、Build、Abstract、Travel，排除 Brand；不从元数据重新生成 SVG。 |
| Carbon Pictograms | `packages/pictograms/README.md` 明确指向仓库根 Apache-2.0；IBM / Carbon contributors | 仅获取该包，按科学、工业、天气和数据相关名称选择 `src/svg`；排除品牌前缀，保留包说明、分类与图案命名元数据。 |

上述各来源的精确提交见 `data/sources.lock.json`，逐图原始链接见 `data/catalog.json` 和 `data/manifest.csv`；完整声明见 `licenses/<source>/`。Carbon 的官方单仓库按 `sparse_paths` 获取所需包，不必拉取其他产品包。

## 本轮未导入的候选与原因

- **GISsymbology 的 `n_arrows` 与 `misc`**：`metadata.ini` 出现 CC BY-SA 2.5，但部分目录许可文件又出现 4.0；为避免错误指定版本，先排除这 58 个 SVG，保留上述四个版本明确的集合。
- **[PSYFI Space Glyphs](https://github.com/p5yb14d3/Icons-Glyphs)**：README 对图标注明 CC BY 4.0，但仓库只有一份包含多个字形的 SVG 字体，缺少可直接预览下载的独立 SVG 图形。本轮未将其算作新增图片库；之后可在明确记录字形提取和改编步骤时再处理。
- **[SBGN Glyph Files](https://github.com/sbgn/glyph-files)**：包含生物网络符号，但未找到明确覆盖这些文件的再分发许可证；“免费、开放社区”描述不足以替代作品许可，本轮不镜像。
- **[Cell Icons](https://github.com/clovestay/cell-icons)**：README 简短，未取得覆盖图形的明确再分发许可，本轮不镜像。
- **[Astronomy Space Icons](https://github.com/mdottavio/astronomy-space-icons)**：该仓库将图形归功于另一名作者，根 MIT 声明与原始图形的授权范围还需交叉核验，本轮不将根代码许可直接套给第三方作品。
- **SwissBioPics / NIH BioArt / IAN 等独立站**：部分已有源码包装器或下载工具，但包装器的代码许可不能替代图片许可；未拿到官方图形和可验证的逐图来源时，只保留检索线索。

本轮通过官方仓库原始 README、许可证、目录结构和实际 SVG 交叉检查；GitHub 搜索一度返回 429 后没有反复重试同一查询。下载量和图库数均不应把仅列链接、字体文件或存在许可范围冲突的候选混入已下载数量。
