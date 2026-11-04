# 天文学与空间科学新增原图审核

核验日期：2026-11-05。本轮从 OpenStax 官方 Astronomy 2e 的固定历史开放版本中新增 **119张原始JPEG，18,455,173字节（17.60 MiB）**。这是新学科来源，不是既有位图的放大或格式转换。

## 固定版本与图像许可

- 官方仓库：[openstax/osbooks-astronomy](https://github.com/openstax/osbooks-astronomy)。
- 唯一选图提交：[`63157f370b09c06a4cc12832384aaaf4de1ced3b`](https://github.com/openstax/osbooks-astronomy/tree/63157f370b09c06a4cc12832384aaaf4de1ced3b)。
- 同一提交的根 [LICENSE](https://github.com/openstax/osbooks-astronomy/blob/63157f370b09c06a4cc12832384aaaf4de1ced3b/LICENSE) 为 Attribution 4.0 International；[README](https://github.com/openstax/osbooks-astronomy/blob/63157f370b09c06a4cc12832384aaaf4de1ced3b/README.md) 将本书按 Creative Commons Attribution 发布。
- [教材 collection](https://github.com/openstax/osbooks-astronomy/blob/63157f370b09c06a4cc12832384aaaf4de1ced3b/collections/astronomy-2e.collection.xml) 明确指向 CC BY4.0；[前言](https://github.com/openstax/osbooks-astronomy/blob/63157f370b09c06a4cc12832384aaaf4de1ced3b/modules/m63293/index.cnxml) 明确允许分发、混编和改编，并要求署名 OpenStax 与内容贡献者。
- 上游2026-03-12随后改为CC BY-NC-SA。本次只取上述历史版本，不把后续非商业版本的新图套用旧许可。

整本教材许可不替代第三方图像权利声明：逐个顶层figure核对图注、标题、媒体alt及原始CNXML，出现 credit、courtesy、modification、adapted、copyright 或 source 标记而未另行核实权利的图像排除。没有因为NASA或其他机构署名就一概认定图片可自由再分发。

## 实际范围与品质

涵盖天球与黄道、行星轨道、季节和地月系统、潮汐与日月食、光谱与辐射、望远镜、行星大气和内部结构、地球板块与磁层、恒星测距与演化、黑洞、星系和宇宙学。

119张均为原生标准位图：长边至少600像素、短边至少200像素，逐图保存真实宽高。适合PPT中的小幅示意图；没有上采样或转换伪SVG，不称为原生高清。

实际原生长边为601–1022像素；没有另外提供虚构的高清版本。

在文本筛选后134张候选中逐张查看3页联系表，再剔除15张未被关键词提前识别的历史肖像/绘画/版画、照片或含照片的合成图，以及纯文字数字表格。最后119张均完成Pillow `verify()`、完整像素解码、原生尺寸及SHA-256检查。与扩充前19,402张目录及来源内部按原始字节SHA去重，没有重复文件。原始像素与文件字节保持不变。

每图保留书内图号、标题、图注、章节CNXML证据路径、真实尺寸、作者、许可、原始路径及哈希。完整目录以本轮导入后的来源清单与全站catalog为准。

## 其他地学候选

`fhemsher/SVG-Earth` 是地学SVG绘图应用，公开仓库中未找到明确再分发许可证，未导入其图形。`titellus/qgis-ian-symbols` 只提供指向IAN原图的QGIS样式XML和一张界面截图，没有保存实际原图或图像许可，因此未将其当作已下载IAN图库。

另外核对了三个地质符号候选：

- `afrigeri/geologic-symbols-qgis` 的大量SVG为既有Daven Quinn图案在三个目录的复制，且collection元数据写CC-BY-SA（未明确版本）、附带LICENSE却为GPL3，未将冲突解释为任选许可后入库。
- `BC-Consulting/FGDC-4-QGIS` 明确按CC0提供图案，但内容主要是已覆盖的同一FGDC标准岩性填充符号，未单凭QGIS格式适配或重复的标准编号增加新图片数。
- `rodreras/geologic_icons` 有716张构造、水文、古生物等SVG及根GPL3文件，但README说明图像是作者2020年下载的USGS文件、未能找到精确原始下载链接；SVG本身未补足原作者与图像许可链。在本轮可核实证据范围内未导入这些图形，也未将README的USGS署名一概替换成公共领域授权。
