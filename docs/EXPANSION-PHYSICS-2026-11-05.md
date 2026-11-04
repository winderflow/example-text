# 2026-11-05：物理、统计与数学原图扩充核验

本分支新增4个OpenStax固定版本来源，选取 **889张原始图片、48,710,926字节（46.45 MiB）**：49张原生长边至少1600像素，840张原生标准位图。未放大图片、未将位图转为伪SVG，也不将自行导出的格式兼容版计为新作品。

| 来源ID与图书 | 本次原图 | 原生高清 | 原生标准 | 固定提交 |
| --- | ---: | ---: | ---: | --- |
| `openstax-physics`，Physics | 90 | 0 | 90 | `1297afa141b898d35c40be2823076f690c238371` |
| `openstax-statistics`，Statistics | 48 | 9 | 39 | `7dea80ae2800386d470b11f6528962f9c4992d15` |
| `openstax-intro-statistics`，Introductory Statistics 2e / Introductory Business Statistics 2e bundle | 339 | 19 | 320 | `50ec91749080bb040b57bb40c34337cacc994cba` |
| `openstax-contemporary-math`，Contemporary Mathematics | 412 | 21 | 391 | `fa7c1a151783958fd2c114da66831e3d57ce2321` |

本表是这4个来源的最终选择数量，全站合计及其他代理新增以重新生成的catalog为准。原生标准图长边600–1599像素、短边至少200像素，适合PPT中较小幅图示；高清图也按实际像素记录，不承诺可无限放大。

## 科研用途和分类

- Physics：受力与矢量、动量和能量、热学与气体、波动、透镜与成像、电路、电磁学、量子与粒子物理等装置和概念示意图。
- Statistics与Introductory Statistics：抽样与实验设计、直方图、箱线图、散点与回归、统计分布、中心极限定理、置信区间、假设检验及方差分析。统计图是教材中的示例图，复用时不能将示例数据冒充自己的实验结果。
- Contemporary Mathematics：集合和逻辑图、函数及不等式模型、概率树、几何与测量、铺砌与空间几何、图论、路径和连通性、网络着色及树结构。重点选取可用于解释方法和模型的图形。

逐图保留原有图注、图号与模块证据，并将原始媒体替代文字放入`alt_text`和检索标签。没有图注的图片使用原始替代文字生成描述性图名，不依据文件编号猜测内容。泛化模块标题还通过原始图号的章节编码补充中文专题分类。

## 图像许可确实适用于内容

4个来源的固定提交根`LICENSE`均为 **Attribution 4.0 International（CC BY4.0）**，README和图书前言也说明是教材内容许可。保留作者OpenStax（Rice University）及内容贡献者的来源信息；每条选图记录包含对应CNXML模块证据路径，未把代码许可套用到图像。

| 官方来源 | 根许可与内容前言 | 历史版本范围 |
| --- | --- | --- |
| [Physics](https://github.com/openstax/osbooks-physics) | [LICENSE](https://github.com/openstax/osbooks-physics/blob/1297afa141b898d35c40be2823076f690c238371/LICENSE)、[前言m54081](https://github.com/openstax/osbooks-physics/blob/1297afa141b898d35c40be2823076f690c238371/modules/m54081/index.cnxml) | 仅使用2026-03-17的固定CC BY4版本。前言明确提醒部分第三方作品另有条件，因此逐图排查署名例外。 |
| [Statistics](https://github.com/openstax/osbooks-statistics) | [LICENSE](https://github.com/openstax/osbooks-statistics/blob/7dea80ae2800386d470b11f6528962f9c4992d15/LICENSE)、[前言m79619](https://github.com/openstax/osbooks-statistics/blob/7dea80ae2800386d470b11f6528962f9c4992d15/modules/m79619/index.cnxml) | 2026-04-23的该固定提交仍明确按CC BY4发布，并不据其他书当前许可推定此书许可。 |
| [Introductory Statistics bundle](https://github.com/openstax/osbooks-introductory-statistics-bundle) | [LICENSE](https://github.com/openstax/osbooks-introductory-statistics-bundle/blob/50ec91749080bb040b57bb40c34337cacc994cba/LICENSE)、[前言m47830](https://github.com/openstax/osbooks-introductory-statistics-bundle/blob/50ec91749080bb040b57bb40c34337cacc994cba/modules/m47830/index.cnxml)、[前言m53808](https://github.com/openstax/osbooks-introductory-statistics-bundle/blob/50ec91749080bb040b57bb40c34337cacc994cba/modules/m53808/index.cnxml) | 使用2026-03-19改为CC BY-NC-SA之前的直接父提交，不取非商业新版素材。 |
| [Contemporary Mathematics](https://github.com/openstax/osbooks-contemporary-mathematics) | [LICENSE](https://github.com/openstax/osbooks-contemporary-mathematics/blob/fa7c1a151783958fd2c114da66831e3d57ce2321/LICENSE)、[前言m00134](https://github.com/openstax/osbooks-contemporary-mathematics/blob/fa7c1a151783958fd2c114da66831e3d57ce2321/modules/m00134/index.cnxml) | 使用2026-03-18改为CC BY-NC-SA之前的直接父提交。 |

根许可、README、前言、各书集合的明确CC BY4.0许可声明以及所选图片对应的CNXML证据应随导入过程保存到各来源的`licenses/`目录。Introductory Statistics与Introductory Business Statistics两本2e均独立核对了集合及前言的内容许可。新图更新必须再次核对固定版本和逐图许可，不能自动跟随默认分支。

## 筛选与重复处理

初筛1,012张候选：Physics114、Statistics72、Introductory Statistics362、Contemporary Mathematics464。全部候选完成Pillow `verify()`、完整`load()`、尺寸及SHA256检查，14页联系表均逐页视觉核对。

额外排除121张视觉不合适的候选，包括未含“credit”关键词但实际注明NASA/Commons/个人来源的照片或外部插画、历史肖像、手机及Excel等软件截图、纯数字/文字表、空白坐标模板和与科研图示用途关系较弱的插画。还手动剔除了4张可确认已经在另一统计学版本保留的同一示例图，避免把明显的版本或格式差异凑为新设计；这4张包含在上述121张中。

对保留候选再做一次完整解码和原始SHA256复核，跨4来源增加精确RGB像素检查，额外排除2张像素完全相同的图片。与基准19,402张原图按原始SHA256去重。所有889张保留原始文件字节，尺寸、作者、许可及模块证据已写入逐图选取清单。未核实独立再分发条件的第三方credit、courtesy、adapted、modification、copyright或source条目在初筛时即排除。

另研究了OpenStax Calculus bundle，但可读取的最早正式根许可已包含非商业条件，因此没有将其混入本轮开放图像。
