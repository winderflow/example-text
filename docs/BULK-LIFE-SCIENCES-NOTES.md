# 生物医学与生命科学原图批量扩充记录

本轮从已经取得并锁定历史许可版本的 OpenStax 官方仓库批量纳入 **1,055 张**科学绘图原文件，新增 **387,475,504 bytes（369.53 MiB）**。这三个来源由 207 张增至 **1,262 张**。以下统计只覆盖本说明的三个来源，其他学科由各自来源记录说明。

| 来源 | 原有 | 新增 | 现有 | 新增原文件 bytes | 新增原生高清 / 标准 |
| --- | ---: | ---: | ---: | ---: | --- |
| 人体解剖与生理 | 184 | 338 | 522 | 206,831,497 | 78 / 260 |
| 生物学综合（含 AP / Concepts） | 20 | 481 | 501 | 116,803,903 | 0 / 481 |
| 微生物学 | 3 | 236 | 239 | 63,840,104 | 0 / 236 |

三来源现有原文件总量为 **536,779,158 bytes**，格式为 **1,136 张 JPEG + 126 张 PNG**。新增 1,055 张中，78 张原生长边至少 1,600 px，977 张属于原生标准分辨率；所有本轮新增图均满足长边至少 600 px、短边至少 200 px。

## 选图与分辨率

保留每个文件的原始字节和真实像素尺寸，没有放大处理，也没有把衍生 PNG 或重复字节计作新的作品。`native-highres` 表示原生长边至少 1,600 px；`native-standard` 表示原生长边 600–1,599 px、短边至少 200 px。标准分辨率图适合 PPT 内的适当尺寸组件，选择整页大图时仍应优先使用原生高清图或 SVG。每条记录都保存宽、高、原文件字节数、SHA256、质量等级及来源图号。

扫描按教材 collection → module → CNXML figure → image 进行，只收录有对应图注及证据路径的科学绘图。保留科学结构图、机制图、流程图、遗传与代谢示意、科学数据图；排除纯表格、段落截图、封面、装饰性图标和不能核实底层许可的摄影/历史作品。没有按固定张数或任意总量截取，符合标准且通过核验的候选均纳入。

全部 1,156 张候选都经过联系表视觉检查，额外排除 101 张：解剖学 11 张、生物学 44 张、微生物学 46 张。排除的具体路径、对应证据及原因写在每份 selection 的 `excluded` 中。

## 许可与固定版本

本轮仅使用以下历史 **CC BY 4.0** 版本；各仓库之后切换许可的版本不用于本次导入。许可证文件、教材前言、collection 与每张图的 CNXML 图注共同提供来源证据。使用图片时应保留 OpenStax（Rice University）及内容贡献者署名、CC BY 4.0 链接和来源链接，并注明是否修改。

| 来源 | 锁定 commit | 主要许可证据 |
| --- | --- | --- |
| [openstax-anatomy](https://github.com/openstax/osbooks-anatomy-physiology/tree/b0058a743bdd2cc08196abaaa7d5469970c0d80c) | `b0058a743bdd2cc08196abaaa7d5469970c0d80c` | `README.md`；`LICENSE`；`modules/m46844/index.cnxml` |
| [openstax-biology](https://github.com/openstax/osbooks-biology-bundle/tree/d2779c2edfb435e75047325434fe2fe93d5aa120) | `d2779c2edfb435e75047325434fe2fe93d5aa120` | `README.md`；`LICENSE`；`modules/m66425/index.cnxml`；`collections/biology-2e.collection.xml`；`modules/m46159/index.cnxml`；`collections/biology-ap-courses.collection.xml`；`collections/concepts-biology.collection.xml`；`modules/m64279/index.cnxml` |
| [openstax-microbiology](https://github.com/openstax/osbooks-microbiology/tree/ecf34dad129d686703780e87ab5aa2e59c577a6a) | `ecf34dad129d686703780e87ab5aa2e59c577a6a` | `README.md`；`LICENSE`；`modules/m63247/index.cnxml`；`collections/microbiology.collection.xml` |

《Concepts of Biology》前言的 Art attribution 还明确说明：未在图注另行提供署名的艺术作品，使用 “Copyright Rice University, OpenStax, under CC BY 4.0 license” 署名。本次没有依据整本教材的默认许可覆盖图注明示的外部作者：出现 credit、courtesy、adapted、modified、版权/供图说明等例外的图片均保守排除；视觉检查识别到未在元数据标注的照片、肖像和旧版画也排除。

## 完整性核验

- 三个缓存仓库 HEAD 均与 selection 固定 commit 一致，所有许可证据文件存在。
- 全部 1,262 张逐文件核验字节数与 SHA256，并使用 Pillow `verify()` 后重新打开完整 `load()`；无损坏文件入选。
- 全部记录的真实尺寸与原文件一致，质量等级与原生尺寸一致。
- 原有 207 张的路径、SHA256、字节数与尺寸全部保留。
- 新增图与已有全站目录按 SHA256 去重，三个本轮来源之间无重复 SHA256；精确字节相同的图片只新增一次。

原生长边范围：人体解剖 609–5,366 px，生物学 600–2,655 px，微生物学 600–1,659 px。

## 排除审计汇总

| 来源 | 外部署名/来源例外 | 尺寸不足 | 元数据照片/扫描 | 表格/文字 | 重复字节 | 解码失败 | 装饰 | 视觉复核额外排除 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 人体解剖与生理 | 138 | 15 | 11 | 25 | 0 | 1 | 0 | 11 |
| 生物学综合（含 AP / Concepts） | 1072 | 326 | 7 | 13 | 20 | 0 | 1 | 44 |
| 微生物学 | 447 | 18 | 37 | 34 | 1 | 0 | 0 | 46 |

审核对象为教材图节点中引用的唯一图片路径。未在相应教材图节点中找到的游离 media 文件，以及没有可追溯图注的装饰资源没有直接导入。排除数量按每个来源内的唯一文件路径统计；已存在的原图保留，不参与本轮新增候选排除计数。
