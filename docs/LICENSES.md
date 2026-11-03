# 素材许可与署名指南

本仓库是多个独立来源的科研绘图素材合集。**下载、整理或部署不会改变原始素材的许可证**，也不表示全库适用同一许可。选择素材前，请查看清单 CSV 与目录数据 JSON 中该素材的作者、来源、许可证名称及版本，并查阅 `licenses/<source>/` 保存的上游许可和说明。清单是检索辅助，原始许可文本与具体素材的权利声明才是判断依据。

“免费使用”不等于允许修改、商业出版或再分发；网站公开展示也不等于开放许可。本库收录的下载素材应有允许再分发的明确依据。仅列为参考链接的资源不代表已下载，未确认许可的图片不应自行混入素材目录。科研论文或商业出版仍需遵守各图的许可和出版方要求。

## 常见许可怎么用

| 许可 | 使用与再分发要点 |
| --- | --- |
| CC0 1.0 | 在适用法律允许的范围内放弃著作权及相关权利，允许复制、修改、再分发与商业使用。著作权许可不强制署名，但论文中保留来源有助于科研可追溯性。 |
| CC BY 3.0 / 4.0 | 允许复制、修改、再分发与商业使用。按具体版本保留作者及其他指定署名信息，提供来源与许可链接；原作提供标题时保留标题，标明自己的修改。不要暗示原作者认可你的研究。 |
| CC BY-SA 3.0 / 4.0 | 除 CC BY 的署名义务外，将改编素材分享给他人时，还需按该许可允许的相同或兼容许可提供改编部分。单纯将原图作为独立作品放入合集，不等于把无关文字或整篇论文自动变成 CC BY-SA；若整幅复合图构成改编作品，需进一步判断共享方式。 |
| ISC / ISC AND MIT | Lucide 新增图标适用 ISC；继承 Feather 的图标还保留 MIT 条件。清单中的 `ISC AND MIT` 表示两个条件共同保留，不表示可任选其一；完整原始声明保存于 `licenses/lucide/LICENSE`。 |
| MIT | 保留上游著作权声明与许可文本；在再分发副本或重要部分时随附。不要只写“MIT”而删除原声明。 |
| BSD | 按具体 BSD 版本保留著作权声明、许可条件与免责声明；涉及二进制再分发时在随附文档中保留要求的信息。若为 BSD 3-Clause，不得未经许可利用作者或组织名称背书。 |
| Apache 2.0 | 保留许可文本和适用声明；上游存在相关 NOTICE 时一并保留。修改文件需作显著说明。其专利授权仅在条款范围内适用，不表示图示技术均可自由实施，也不授权使用商标。 |

同一个项目也可能有多种许可。例如图标、字体、网站代码可能各用不同许可；不能用网站代码的 MIT 许可替代图标的 CC BY 许可。Bioicons 等聚合库尤其需要逐图查看，不能把平台许可直接套用到每张图。

## 论文署名示例

以下是格式示例，请替换为该素材实际提供的信息：

> “Original asset title”，作者姓名或机构，来源：原始作品链接，采用 CC BY 4.0（https://creativecommons.org/licenses/by/4.0/）。修改：调整配色与裁剪。

若图中使用了多个来源，可以在图注、致谢或随附的素材清单中逐项记录。引用本仓库不能替代对原作者的署名。下载单张 SVG 后，请同时保存该条目的来源、作者及许可记录；SVG 文件本身未必包含完整署名信息。

## 著作权以外的权利

开放著作权许可通常不提供商标、肖像、隐私、专利或第三方标识的全面授权。科研软件品牌图标仍可能受商标规则限制；红十字、红新月等受保护医疗标志也不应仅凭 SVG 的开放许可随意用于标识产品或机构。图中涉及人物、标志或受保护符号时，应结合实际用途核查。

素材是绘图组件，不是医学结论或解剖准确性的保证。发表前应由研究者检查科学含义、适用性和原作说明。

## 其他官方资源及收录状态

以下项目可补充科研流程图、计算机架构图和数据示意图。2026-11-03 已将 Lucide、Font Awesome、Bootstrap 和 IconPark 的科研相关选集实际入库；Google Material 与 Simple Icons 仍仅列链接，未计入下载数量。具体文件数量以目录清单为准。

| 官方项目 | 可用于科研绘图的内容及状态 | 许可依据与注意事项 |
| --- | --- | --- |
| [Lucide](https://github.com/lucide-icons/lucide) | 显微镜、原子、数据库、网络、仪器等线性图标；已收科研选集 | [完整 LICENSE](https://github.com/lucide-icons/lucide/blob/main/LICENSE)：ISC；继承自 Feather 的部分图标还保留 MIT 声明。 |
| [Font Awesome Free](https://github.com/FortAwesome/Font-Awesome) | 实验器材、化学、医学、工程与流程图标；已收非品牌科研选集 | [LICENSE.txt](https://github.com/FortAwesome/Font-Awesome/blob/7.x/LICENSE.txt)：SVG/JS 图标 CC BY 4.0；字体另用 OFL，代码另用 MIT。品牌图标另注意商标。 |
| [Google Material Icons / Symbols](https://github.com/google/material-design-icons) | 科学、教育、设备、环境、地图与数据图标 | [LICENSE](https://github.com/google/material-design-icons/blob/master/LICENSE)：Apache 2.0。仓库体积较大，宜按主题和样式筛选。 |
| [Bootstrap Icons](https://github.com/twbs/icons) | 图表、数据库、设备与科研工作流图标；已收科研选集 | [LICENSE](https://github.com/twbs/icons/blob/main/LICENSE)：MIT。 |
| [IconPark](https://github.com/bytedance/IconPark) | 设备、数据、交通、工业图标；已收含中文元数据的选集 | [LICENSE](https://github.com/bytedance/IconPark/blob/master/LICENSE)：Apache 2.0。 |
| [Simple Icons](https://github.com/simple-icons/simple-icons) | 科研软件、编程工具和计算平台的品牌标志 | [LICENSE.md](https://github.com/simple-icons/simple-icons/blob/develop/LICENSE.md)：CC0；品牌商标权仍需另查，不代表获得品牌背书。 |

本说明是使用辅助，不替代具体许可证原文。若清单、上游文件或素材内声明存在冲突，应先回到上游核实，再决定是否使用或再发布。
