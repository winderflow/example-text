# OpenStax 解剖与生理原始插图来源核验

截至2026-11-04，当前共收录 **522张原始插图，341,830,016字节**（519张JPEG、3张PNG）：其中262张为原生高清 `native-highres`，260张为原生标准 `native-standard`。原生高清长边至少1600px；原生标准长边600–1599px、短边至少200px。当前原生长边范围609–5366px，文件保持原始字节与像素尺寸，没有放大处理。

本次批量扩充新增338张，包含78张原生高清与260张原生标准图；具体筛选、视觉复核与许可审计见[批量扩充记录](BULK-LIFE-SCIENCES-NOTES.md)。标准图适合PPT内的适当尺寸组件，整页大图应优先使用原生高清或SVG。

早期高清批次于2026-11-03开始核验，选取官方《Anatomy and Physiology 2e》固定历史版本的原始高清JPEG。下文保留该批次的历史数字；1600px是当时的筛选门槛，不是当前全部图片的最低长边。

## 固定版本与许可范围

- 官方仓库：<https://github.com/openstax/osbooks-anatomy-physiology>。
- 本轮唯一来源提交：[`b0058a743bdd2cc08196abaaa7d5469970c0d80c`](https://github.com/openstax/osbooks-anatomy-physiology/tree/b0058a743bdd2cc08196abaaa7d5469970c0d80c)。
- 该提交的 [LICENSE](https://github.com/openstax/osbooks-anatomy-physiology/blob/b0058a743bdd2cc08196abaaa7d5469970c0d80c/LICENSE) 明确为 **CC BY 4.0**。
- 同一提交的 [README](https://github.com/openstax/osbooks-anatomy-physiology/blob/b0058a743bdd2cc08196abaaa7d5469970c0d80c/README.md) 将教材按 Creative Commons Attribution 发布；[前言模块](https://github.com/openstax/osbooks-anatomy-physiology/blob/b0058a743bdd2cc08196abaaa7d5469970c0d80c/modules/m46844/index.cnxml) 明确说明教材采用 CC BY 4.0，可分发、改编并署名 OpenStax 与内容贡献者。这些是教材内容的许可依据，不是软件代码许可。

**当前主分支不是本次图源。** 上游于2026-03-19的 [`fdfa6e21ac3bc372dc2802a9952df124a619fdcc`](https://github.com/openstax/osbooks-anatomy-physiology/commit/fdfa6e21ac3bc372dc2802a9952df124a619fdcc) 将 LICENSE、README 和前言改为 CC BY-NC-SA 4.0。本轮只使用此前已明确按 CC BY 4.0 发布的固定历史文件，不从后续版本取新图并套用旧许可。

## 早期高清批次（历史记录）

选择清单：[`data/source-selections/openstax-anatomy.json`](../data/source-selections/openstax-anatomy.json)。

- 首批117张原始JPEG为73,120,867字节；2026-11-04的下一高清批次增加67张，当时累计 **184张、134,998,519字节**。这些图片均保留在当前522张清单中，原始字节与实际像素尺寸不变。
- 上述184张的原始长边 **1602–3166 像素**，没有上采样。按章节覆盖人体器官、细胞、组织、骨骼肌肉、神经、血液循环、免疫、呼吸、消化、泌尿和生殖发育等主题。
- 每图记录原始文件路径、图题、图注、章节主题、图号、对应 CNXML 证据模块、原始像素尺寸和 SHA-256。署名为 **OpenStax (Rice University)**，保留教材及内容贡献者的来源信息。
- 仅选择图形所在 CNXML 中未出现外部第三方署名或来源例外的教材插图；不将出版社对整本教材的默认许可覆盖到明确另有署名的第三方图像。
- 早期高清批次排除明确的第三方 credit / courtesy / modification-of-work 标记、照片或显微图、扫描图、表格图及低于原始1600像素阈值的候选。当前批量收录仍逐图检查来源例外，并将满足600px长边、200px短边的清晰科学绘图按真实分辨率分级。另发现一张源 JPEG 无法完整解码，保持原件不变并排除，没有关闭解码校验。

挑选没有修改像素、裁剪内容或移除图片内标注。JPEG/PNG本身不是可编辑矢量图，但可直接插入 PowerPoint；需要重新布局文字时应在所用软件中另行编辑，并按许可注明修改。

## 维护要求

更新该来源时必须重新检查许可证和逐图来源；不能让默认分支自动取代本轮固定提交。保留 LICENSE、README、前言以及所选图形对应的 CNXML 元数据，避免未来读者只能看到新版本许可而失去本轮授权证据。
