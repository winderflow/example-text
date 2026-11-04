# OpenStax 生物学原始插图来源核验

截至2026-11-04，当前共收录 **501张原始插图，128,891,629字节**（123张PNG、378张JPEG），覆盖同一固定历史版本中的《Biology 2e》《Biology for AP Courses》和《Concepts of Biology》。其中20张为原生高清 `native-highres`，481张为原生标准 `native-standard`：原生高清长边至少1600px；原生标准长边600–1599px、短边至少200px。当前原生长边范围600–2655px，均保留原始尺寸，没有上采样。

本次批量扩充新增481张，涵盖生命化学、细胞与信号、代谢、遗传、植物、动物生理、进化与生态。原始PNG/JPEG可直接插入PowerPoint；标准图适合适当尺寸组件，整页大图优先选择原生高清或SVG。完整审核见[批量扩充记录](BULK-LIFE-SCIENCES-NOTES.md)。

早期高清批次收录20张《Biology 2e》原件，以下保留其历史统计；1600px是该批次的门槛，不是当前501张的统一最低长边。

## 固定版本与教材许可

- 官方仓库：<https://github.com/openstax/osbooks-biology-bundle>。
- 唯一图像版本：[`d2779c2edfb435e75047325434fe2fe93d5aa120`](https://github.com/openstax/osbooks-biology-bundle/tree/d2779c2edfb435e75047325434fe2fe93d5aa120)。
- 该版本的 [LICENSE](https://github.com/openstax/osbooks-biology-bundle/blob/d2779c2edfb435e75047325434fe2fe93d5aa120/LICENSE) 开头为“**Attribution 4.0 International**”，即CC BY 4.0。
- 同版本 [README](https://github.com/openstax/osbooks-biology-bundle/blob/d2779c2edfb435e75047325434fe2fe93d5aa120/README.md) 将教材按Creative Commons Attribution发布。
- 《Biology 2e》[前言模块](https://github.com/openstax/osbooks-biology-bundle/blob/d2779c2edfb435e75047325434fe2fe93d5aa120/modules/m66425/index.cnxml) 明确写明：“Biology 2e is licensed under a Creative Commons Attribution 4.0 International (CC BY) license, which means that you can distribute, remix, and build upon the content, as long as you provide attribution to OpenStax and its content contributors.”
- 同版本的[教材集合元数据](https://github.com/openstax/osbooks-biology-bundle/blob/d2779c2edfb435e75047325434fe2fe93d5aa120/collections/biology-2e.collection.xml) 也将内容许可链接指向`http://creativecommons.org/licenses/by/4.0/`。早期20张只从该集合引用的Biology 2e模块选图。当前扩充同时扫描同版本的AP与Concepts集合，逐图保留CNXML原始图注、替代文字及所属模块路径。

《Biology for AP Courses》的[前言模块m64279](https://github.com/openstax/osbooks-biology-bundle/blob/d2779c2edfb435e75047325434fe2fe93d5aa120/modules/m64279/index.cnxml)和《Concepts of Biology》的[前言模块m46159](https://github.com/openstax/osbooks-biology-bundle/blob/d2779c2edfb435e75047325434fe2fe93d5aa120/modules/m46159/index.cnxml)同样明确CC BY 4.0。Concepts前言的Art attribution还明确：未另列署名的图应署名“Copyright Rice University, OpenStax, under CC BY 4.0 license”。这些前言及相应collection已加入当前selection的许可证据。

上游于2026-03-19在提交[`4ea6132f7acb0fc9ef1015b11a59427fd7b4c61c`](https://github.com/openstax/osbooks-biology-bundle/commit/4ea6132f7acb0fc9ef1015b11a59427fd7b4c61c)将许可改为CC BY-NC-SA。这里固定为该修改的直接父提交，使用之前已经明确按CC BY 4.0发布的原始文件；后续版本的新图不自动纳入，也不套用旧许可。

## 早期20张高清批次（历史记录）

完整机器清单：[`data/source-selections/openstax-biology.json`](../data/source-selections/openstax-biology.json)。

- 该批次为 **20张**原件：19张PNG、1张JPEG，合计**12,087,726字节**；全部保留在当前501张清单中。
- 这20张的原始长边**1600–2655像素**，没有上采样。分类为生物医学14张、化学与分子3张、生态与物种3张。
- 逐图记录中文与英文标题、图号、原始路径、图注、主题、许可、CNXML证据、原生尺寸、字节数和SHA-256。
- 每一原件均通过Pillow `verify()`与重新打开后的完整`load()`解码；保持正常损坏检查，没有跳过解码错误。
- 逐图检查图形CNXML，不收录存在第三方credit、courtesy、modification-of-work、copyright等来源例外的图形。默认教材许可只用于未标注外部来源的出版社插图。
- 当时筛选排除664个带外部署名或来源例外的候选、435个原生长边不足1600像素的候选、25个纯图表候选、5个照片或显微图候选及1个书内字节重复候选。这是早期高清批次的历史统计；当前逐项排除原因见selection，清晰科学数据图可作为科学绘图收录，纯表格和段落截图仍排除。
- 与导入前整个图库的原件SHA-256进行核对，所选20张没有字节重复。所有20张另经接触表目视检查，均为绘制的科学插图或实验流程示意。

这些是位图原件，图片内文字不会在PowerPoint中自动成为可编辑文本。转载或改编时应按CC BY 4.0保留OpenStax、内容贡献者、准确的固定版本来源与许可链接；修改后说明修改。

## 维护

继续更新时必须固定提交并重新核验教材及逐图来源。保留LICENSE、README、前言、集合元数据和每图引用的CNXML，以便主分支许可发生变化后仍可核对本轮原始发布依据。
