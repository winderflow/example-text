# OpenStax 微生物学原始高清插图来源核验

核验日期：2026-11-04。本轮选择 OpenStax 官方《Microbiology》固定历史版本中的原始 JPEG，按原始尺寸下载，没有将低分辨率图片放大后充当高清素材。

## 固定版本与教材许可

- 官方仓库：<https://github.com/openstax/osbooks-microbiology>。
- 本轮唯一来源提交：[`ecf34dad129d686703780e87ab5aa2e59c577a6a`](https://github.com/openstax/osbooks-microbiology/tree/ecf34dad129d686703780e87ab5aa2e59c577a6a)。
- 该提交的 [LICENSE](https://github.com/openstax/osbooks-microbiology/blob/ecf34dad129d686703780e87ab5aa2e59c577a6a/LICENSE) 明确为 **CC BY 4.0**；同一版本的 [README](https://github.com/openstax/osbooks-microbiology/blob/ecf34dad129d686703780e87ab5aa2e59c577a6a/README.md) 将《Microbiology》按 Creative Commons Attribution 发布。
- [前言模块 m63247](https://github.com/openstax/osbooks-microbiology/blob/ecf34dad129d686703780e87ab5aa2e59c577a6a/modules/m63247/index.cnxml) 直接说明教材采用 Creative Commons Attribution 4.0 International，允许分发、改编和再创作，并要求署名 OpenStax 及其内容贡献者。[教材集合元数据](https://github.com/openstax/osbooks-microbiology/blob/ecf34dad129d686703780e87ab5aa2e59c577a6a/collections/microbiology.collection.xml) 同样声明 CC BY 4.0。这些是教材内容的授权证据。

上游于2026-03-19的 [`f1d8d4e9941417f25610a239045c35488d56cf22`](https://github.com/openstax/osbooks-microbiology/commit/f1d8d4e9941417f25610a239045c35488d56cf22) 将许可改为 CC BY-NC-SA。本轮固定于该许可变更的直接父提交，仅取此前已按 CC BY 4.0 发布的原始文件，不从后续版本取图后套用旧许可。

## 实际选择与排除

选择清单：[`data/source-selections/openstax-microbiology.json`](../data/source-selections/openstax-microbiology.json)。

- **3张原始 JPEG**，合计 **2,217,409 字节**。
- 原始像素分别为 **1200×1605、1155×1608、1332×1659**，原始长边均超过1600像素。
- 主题为细菌转化与分子克隆流程、补体结合试验流程、消化系统与胃肠道解剖。每图保留图注、图号、CNXML 证据模块、文件路径、像素尺寸及 SHA-256。
- 署名为 **OpenStax (Rice University)**，并保留教材内容贡献者的来源信息。所选图形所在 CNXML 未包含第三方 credit、courtesy、改编来源或版权例外。
- 全书扫描排除445个出现第三方来源标记的图文件、308个低于原始1600像素阈值的文件、34个照片或显微图文件、5个图表候选；另外对6个初筛高清候选制作联系表并进行目视检查，排除3张以表格为主体的图片，保留3张科学插图。没有为增加数量放宽原始分辨率或许可筛选。
- 每张入选 JPEG 均执行 Pillow `verify()` 并重新打开、完整 `load()` 解码，检查原始尺寸与 SHA-256；没有关闭图像验证。选择时亦与现有图库 SHA-256 去重。

文件未经裁剪、放大、重绘或移除文字。JPEG 可直接插入 PowerPoint；其中文字不作为可单独编辑的矢量对象提供。使用时按 CC BY 4.0 署名并提供来源及许可链接，改编后注明修改。

## 后续维护

固定源提交及选择清单应一并保留。每次扩展必须重新检查教材许可和逐图来源；保持 README、LICENSE、前言、教材集合元数据与图形对应 CNXML 证据可追溯，避免当前主分支的新许可替代这次历史授权依据。
