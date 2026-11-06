# 2026-11-06：SBGN专业生物过程图形核验

本轮新增来源候选为SBGN当前官方站点仓库，实际选择 **48张原始SVG、643,766字节**：19个独立生物过程符号、24张规范示例、1张区室示例、3张参考图板，以及1幅完整iNOS通路图。它们是SVG原件，不是把SBGN/GPML数据重新渲染后当作新原图计数。

## 固定来源与许可

- 仓库：[sbgn/sbgn.github.io](https://github.com/sbgn/sbgn.github.io)。
- 固定提交：[`d2cc88d34863ebd8cb1e6815ed9e0e07d2555b80`](https://github.com/sbgn/sbgn.github.io/tree/d2cc88d34863ebd8cb1e6815ed9e0e07d2555b80)。
- 同一版本的[根LICENSE](https://github.com/sbgn/sbgn.github.io/blob/d2cc88d34863ebd8cb1e6815ed9e0e07d2555b80/LICENSE)为 **CC0 1.0 Universal**。
- [README](https://github.com/sbgn/sbgn.github.io/blob/d2cc88d34863ebd8cb1e6815ed9e0e07d2555b80/README.md)说明`Downloads`目录用于存放SVG、PNG、SBGN等格式的图形；[符号页](https://github.com/sbgn/sbgn.github.io/blob/d2cc88d34863ebd8cb1e6815ed9e0e07d2555b80/pages/symbols.md)与[参考图板页](https://github.com/sbgn/sbgn.github.io/blob/d2cc88d34863ebd8cb1e6815ed9e0e07d2555b80/pages/referencecards.md)明确提供这些图形用于学习和绘图。

作者按SBGN community contributors保留机构/社区署名，没有为不含个人画师元数据的图形补造个人作者。即使CC0不要求著作权署名，科研使用仍建议保留SBGN标准、具体图形来源及版本。

旧仓库`sbgn/sbgn`的根MIT许可声明属于网站主题，其作者为主题开发者；没有拿它作为本批科学图片的许可依据。没有许可文件的`sbgn/glyph-files`独立仓库也没有直接镜像。

## 选择与使用范围

图形包括macromolecule、nucleic-acid feature、complex、compartment、生物过程及其消耗/生成、催化、调节、刺激、抑制和逻辑连接等。规范示例展示状态变量、克隆标记、节点分类、边分类和布局关系。

参考图板沿用固定版本官方页面列出的AF L1V1.2、ER L1V2.0、PD L1V2.0文件，保留原有版本名；不据此声称所有SBGN规范截至今日均以这些版本为最新。完整版iNOS示例保留区室、分子状态、连接和全部文字标注。

`layout-orientation.svg`原作包含wrong/correct对照，目录明确写成“正例与反例对照”；使用时应保留原注释。单独展示错误布局的`compartment_overlapping_wrong.svg`未收录。全部SVG保持原字节，未删标签、裁剪或擅自更改配色。

## 核验结果

- 48张逐图通过原始SHA256、现有图库SHA去重、XML及被动SVG检查。
- 逐图检查CSS外部`url()`与`@import`，没有引入外部资源的依赖。
- 48张全部由Inkscape在白底上渲染成功，并目视检查2页联系表，未发现空白、缺字、失效符号或外部图片缺失。
- 源检出目录保持干净，固定提交与选择清单一致。内部渲染图只用于检查，不计作新图片，也未替换原SVG。

## 没有计入的素材

Inkscape保存副本、旧参考图板版本、字体、品牌图标和同一iNOS通路的黑白/另一编辑器渲染版本均未重复计数。明确引用Nature Reviews Genetics原论文的`lenovere_representations.png`、第三方KEGG巨图及工具竞赛截图没有凭网站CC0就推定可再分发。

另检查了WikiPathways官方`sandbox-wp-assets`（只有4幅SVG且未获得独立许可证据）、MD Anderson的`pathway-diagrams`（只有Newt/SBGN模型，无原始SVG/PNG）、libSBGN（软件及测试模型）和SBGN Open Challenge（主要为模型及外部集合）。这些没有以“生成图片”或“多格式副本”的方式凑入新增原图数。

继续检查了SysBio Curie的NaviCell。仓库看似有1,443个SVG，但大部分属于Bootstrap及编辑器界面图标；地图PNG存在多级分辨率、透明背景等重复副本，而根LGPL软件许可没有单独闭合各张外来地图的授权链。这些没有算作新的科研图片库或额外通路图。

选择清单由父任务规范化后保存到`data/source-selections/sbgn-scientific-diagrams.json`；实际入库数量以更新后的全库目录为准。
