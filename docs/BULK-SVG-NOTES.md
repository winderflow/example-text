# 完整科研 SVG 批量扩展核验

核验日期：2026-11-04。本轮取消此前为控制网页发布包体积设置的 Reactome 90 MiB 选图上限，补齐同一官方固定版本中符合本库被动预览规则的完整通路 SVG。原始文件仍完整保存在仓库；发布包的大图交付由主站构建流程处理。

## Reactome 完整生物通路图

- 官方仓库：[reactome/reactome_illustrations](https://github.com/reactome/reactome_illustrations)。
- 唯一固定提交：[`9b70b1d706086d3d917f4150ab59aa65815b3c47`](https://github.com/reactome/reactome_illustrations/tree/9b70b1d706086d3d917f4150ab59aa65815b3c47)。
- [README](https://github.com/reactome/reactome_illustrations/blob/9b70b1d706086d3d917f4150ab59aa65815b3c47/README.md) 明确说明 `ehld/` 保存完整 EHLD 生物通路 SVG，`statics/` 保存静态生物过程示意图；并非只给网站代码贴上许可后推定图片开放。
- [根 LICENSE](https://github.com/reactome/reactome_illustrations/blob/9b70b1d706086d3d917f4150ab59aa65815b3c47/LICENSE) 为 Apache License 2.0。保留许可证、文件内已有署名及作品标识，作者记为 Reactome illustration contributors；没有为缺少个人画师元数据的整幅图臆造作者姓名。

源目录共有221张EHLD与35张静态图。本轮逐图重新核对XML格式、脚本、事件处理器、外部图像引用及原始SHA-256后，保留 **255张**：220张EHLD、35张静态示意图，共 **132,845,902字节**。此前164张已经公开收录的文件保持原字节不变，**本轮新增91张完整SVG**；这仍是既有Reactome来源的扩充，不算91个新图库，也不把不同格式转换重复计为新图。

唯一继续排除的文件为 `ehld/R-HSA-9859713.svg`：包含尚未逐项审核的 `foreignObject` 内容。没有通过删改文件后再声称“原图未修改”，也没有为了增加数量关闭被动SVG检查。

实际选图清单、原始哈希、官方R-HSA编号、参考页面与可从SVG中直接取得的标签见 [`data/source-selections/reactome-pathways.json`](../data/source-selections/reactome-pathways.json)。没有取得可核实标题时保留官方编号，不根据路径编号猜测具体生物过程名称。

## 下载与使用

这些是完整科研插画与示意图，适合在论文、海报或PPT中按需引用和组合；它们不是每一处文字都能在Office中单独编辑的图形。原始SVG保留其原始画布和作品内全部标注。文件内若包含位图部分，其细节仍受原图限制；不能只凭SVG扩展名承诺每个组成部分均为无限分辨率矢量。

复用时保留Apache2.0许可与适用署名；如有修改应标明。图库下载记录不替代研究者对通路内容、版本与研究适用性的核查。

## 新核实的实验仪器插画来源：CPM LabIcons

另取得并核实官方 [Center-for-Proteomics-and-Metabolomics/LabIcons](https://github.com/Center-for-Proteomics-and-Metabolomics/LabIcons) 固定提交 [`d212e350f6f4e3cd60f48da5c97207f0cb1f26bb`](https://github.com/Center-for-Proteomics-and-Metabolomics/LabIcons/tree/d212e350f6f4e3cd60f48da5c97207f0cb1f26bb)。这是人工绘制的科学仪器插画，不是通用界面图标。

- [equipment/README.md](https://github.com/Center-for-Proteomics-and-Metabolomics/LabIcons/blob/d212e350f6f4e3cd60f48da5c97207f0cb1f26bb/equipment/README.md) 对文件逐项列出作者与CC BY4.0授权；根 [LICENSE.md](https://github.com/Center-for-Proteomics-and-Metabolomics/LabIcons/blob/d212e350f6f4e3cd60f48da5c97207f0cb1f26bb/LICENSE.md) 保存许可全文。
- 可用候选为 **10张原生透明PNG**，长边974–1571像素。它们是适合适度尺寸排版的原始科研部件图，**不标为1600像素以上高清原件**，也没有插值放大。
- 9张署名Manon Zuurmond；`solarix.png`署名Stefan Ruchti，应保留逐图作者覆盖信息，不能把顶层署名示例统一套给全部文件。
- 11张原始PNG中的 `easy_nlc.png` 为468×527像素，未满足本轮600像素长边标准，因此排除。所有10个合格原件完成像素解码和SHA-256检查，与既有合集没有相同原始字节或相同作者条目。
- 仓库另提供可编辑Illustrator `.ai` 原稿；它们不是可直接插入PowerPoint的SVG，也不重复计为额外图片。

本轮已将这10张透明PNG实际入库，记录包含作者ORCID、原图地址、许可证据与真实像素；下载目录见[本批索引](BULK-OPEN-ART-2026-11-04.md)，来源清单为[`cpm-labicons.json`](../data/source-selections/cpm-labicons.json)。Illustrator原稿在上游对应固定提交中另行提供。

## 未计入的其他候选

- `eamonnmag/biocons` 仅发现一张Illustrator分类学整版，没有可直接预览的独立SVG或PNG图片集合，未以“图库数量”计入。
- SciGlyph虽然声称有数千张CC BY4 SVG，但其内容为AI辅助图形，尚未逐项核验科研机制与安全符号准确性；没有仅凭数量与README声明把它们归为已核验科研原图。
