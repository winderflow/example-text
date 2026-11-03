# OpenStax 解剖与生理高清插图来源核验

核验日期：2026-11-03。本轮选取的是 OpenStax 官方《Anatomy and Physiology 2e》固定历史版本中的原始高清 JPEG，不是网站界面截图，也没有将小图放大后当成高清原件。

## 固定版本与许可范围

- 官方仓库：<https://github.com/openstax/osbooks-anatomy-physiology>。
- 本轮唯一来源提交：[`b0058a743bdd2cc08196abaaa7d5469970c0d80c`](https://github.com/openstax/osbooks-anatomy-physiology/tree/b0058a743bdd2cc08196abaaa7d5469970c0d80c)。
- 该提交的 [LICENSE](https://github.com/openstax/osbooks-anatomy-physiology/blob/b0058a743bdd2cc08196abaaa7d5469970c0d80c/LICENSE) 明确为 **CC BY 4.0**。
- 同一提交的 [README](https://github.com/openstax/osbooks-anatomy-physiology/blob/b0058a743bdd2cc08196abaaa7d5469970c0d80c/README.md) 将教材按 Creative Commons Attribution 发布；[前言模块](https://github.com/openstax/osbooks-anatomy-physiology/blob/b0058a743bdd2cc08196abaaa7d5469970c0d80c/modules/m46844/index.cnxml) 明确说明教材采用 CC BY 4.0，可分发、改编并署名 OpenStax 与内容贡献者。这些是教材内容的许可依据，不是软件代码许可。

**当前主分支不是本次图源。** 上游于2026-03-19的 [`fdfa6e21ac3bc372dc2802a9952df124a619fdcc`](https://github.com/openstax/osbooks-anatomy-physiology/commit/fdfa6e21ac3bc372dc2802a9952df124a619fdcc) 将 LICENSE、README 和前言改为 CC BY-NC-SA 4.0。本轮只使用此前已明确按 CC BY 4.0 发布的固定历史文件，不从后续版本取新图并套用旧许可。

## 实际选择

选择清单：[`data/source-selections/openstax-anatomy.json`](../data/source-selections/openstax-anatomy.json)。

- 117张未经改写的原始 JPEG，合计 **73,120,867 字节**，受70 MiB预算限制；准确字节值以选择清单的 `selected_bytes` 为准。
- 原始长边 **1602–3000 像素**，没有上采样。按章节覆盖人体器官、细胞、组织、骨骼肌肉、神经、血液循环、免疫、呼吸、消化、泌尿和生殖发育等主题。
- 每图记录原始文件路径、图题、图注、章节主题、图号、对应 CNXML 证据模块、原始像素尺寸和 SHA-256。署名为 **OpenStax (Rice University)**，保留教材及内容贡献者的来源信息。
- 仅选择图形所在 CNXML 中未出现外部第三方署名或来源例外的教材插图；不将出版社对整本教材的默认许可覆盖到明确另有署名的第三方图像。
- 排除明确的第三方 credit / courtesy / modification-of-work 标记、照片或显微图、扫描图、表格图及低于原始1600像素阈值的候选。另发现一张源 JPEG 无法完整解码，保持原件不变并排除，没有关闭解码校验。

挑选没有修改像素、裁剪内容或移除图片内标注。JPEG本身不是可编辑矢量图，但可直接插入 PowerPoint；需要重新布局文字时应在所用软件中另行编辑，并按许可注明修改。

## 维护要求

更新该来源时必须重新检查许可证和逐图来源；不能让默认分支自动取代本轮固定提交。保留 LICENSE、README、前言以及所选图形对应的 CNXML 元数据，避免未来读者只能看到新版本许可而失去本轮授权证据。
