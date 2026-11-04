# SBOL Visual 合成生物学图形核验（2026-11-05）

官方来源为 [SynBioDex/SBOL-visual](https://github.com/SynBioDex/SBOL-visual)，本轮固定提交 [`f6b2f53a22105c768d376ecf68d67cc7f4516115`](https://github.com/SynBioDex/SBOL-visual/tree/f6b2f53a22105c768d376ecf68d67cc7f4516115)。这些是用于表示遗传设计、核酸特征、分子物种和相互作用的标准化科研符号，不是解剖器官插画。

## 图形许可与分类

根 [`LICENSE.html`](https://github.com/SynBioDex/SBOL-visual/blob/f6b2f53a22105c768d376ecf68d67cc7f4516115/LICENSE.html) 明确规定：除列出的例外外，整个作品采用 **CC BY4.0**；SBOL开发者对 **SBOL Visual glyphs** 采用 **CC0 1.0** 权利放弃。该许可明确针对作品与图形，不是将软件代码许可推定为图片许可。

独立glyph采用CC0，基因线路示例及sampler总览保留默认CC BY4.0。作品作者记为SBOL Visual developers and contributors；每图保留固定版本原作地址和对应glyph说明或sampler README作为来源证据。CC BY示例与总览复用时需保留作者、来源和许可；CC0符号仍建议在论文中保留标准来源引用。

收录范围包括相互作用节点、控制/降解/抑制/促进等作用箭头、DNA/RNA/蛋白质与小分子、启动子、编码序列、终止子、限制性位点、复制起点、结合位点和基因线路示例。原始SVG保持全部线条、文字、颜色和原始画布。

## 逐图渲染与范围复核

初始候选清单共78张：64张glyph、14张示例或总览。全部原文件执行SHA-256核验、XML解析及本库被动SVG检查；随后用Inkscape逐张导出白底核验PNG，**78张均成功渲染，未发现空白图、文字缺失、未加载图像或断裂线路**。全部核验图组成3页联系表并逐页视觉审查。PNG只用于审查，不作为额外新图片计数，也未替换原始SVG。

核验发现 `sampler/Deprecated.svg` 明确是过时符号总览，含旧Insulator和Macromolecule图形。它虽可正常渲染且有许可，但与本批排除deprecated符号的范围不符，因此建议从正式新增目录排除。排除此图后，建议范围为 **77张SVG：64张CC0独立glyph、13张CC BY4.0示例/总览**，最终收录数量以主目录为准。

其余4张总览分别为Interaction Nodes、Interactions、Molecular Species和Sequence Features，可以正常查看；图内有较小标签，使用时宜打开原始SVG并按需要放大。染色体、环状质粒、内含子及多肽示例中的线路和文字均可显示。符号本身是语义组件，单张简单圆形、箭头或矩形仍应结合具体glyph说明使用，不能只按外形猜测其生物学含义。

`-specification.svg` 边框/定位标注页及deprecated目录不作为新增科研单图。固定版本的原始许可、README和逐图说明随清单保留；没有为了使渲染通过修改原件、删除标注或关闭SVG安全检查。
