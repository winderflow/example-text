# 专题SVG与显微光学原图扩充核验

核验日期：2026-11-05。本记录涵盖本轮五个新来源中实际取得并审核的 **187张原件**：158张SVG、27张PNG与2张JPEG。位图含19张原生高清和10张原生标准图，均保留原始字节，没有放大或把格式转换重复计为新图。全站本轮合计以主索引及重新生成的目录为准。

## 科研流程与专题地图SVG

| 来源 | 本轮选择 | 许可 | 范围 |
| --- | ---: | --- | --- |
| [PEC Process Map Vector Graphics](https://github.com/PEC-Development-Team/Process-Map-Vector-Graphics/tree/e30c9f919d93fe099c49ee15c0b97b1647a84711) | 51 | MIT | 6张BPMN、6张DFD、14张UML/ERD、25张流程形状 |
| [OpenStreetMap Carto科研专题](https://github.com/gravitystorm/openstreetmap-carto/tree/003cefdd67918e8317e9753312ec3327d78f5d1f) | 107 | CC0-1.0 | 植被地表29、地形14、能源/通信/天文观测25、健康医疗9、其他环境设施30 |

PEC仓库主体就是流程图矢量图形，根MIT许可覆盖所分发素材；作者保留PEC Development Team。没有再次计算其PNG、EMF、AI、整版海报和PPTX中的同一图形。上游另有可直接使用的Process-Map-Symbols.pptx，作为可选外部参考，不计新图。

OSM Carto根`LICENSE.txt`明确CC0 1.0，并特别声明包括cartographic design；作者按上游声明记录Andy Allan、Steve Chilton与贡献者。未收660张重复尺度公路编号空白盾牌及商店、娱乐、宗教等无关主题；一个相同字节的`scree.svg`排除。选集为科学地图的符号与填充组件，不将它们描述成复杂机制插画。

158张SVG全部通过被动内容检查、SHA-256去重、Chromium实际渲染以及联系表视觉检查，没有脚本、事件处理器、未审核foreignObject或外部图像依赖。

## York Lab开放显微光学原图

| 官方研究仓库与固定版本 | 本轮选择 | 原生高清 / 标准 | 原件字节数 |
| --- | ---: | ---: | ---: |
| [Remote refocus](https://github.com/AndrewGYork/remote_refocus/tree/284efac5354fdfdd4a6dc2dc21c68e06eea53c7c) | 5 | 2 / 3 | 1,131,269 |
| [High-NA single-objective light-sheet](https://github.com/AndrewGYork/high_na_single_objective_lightsheet/tree/46a205567133d98b188af112b857751b91f6c13c) | 22 | 16 / 6 | 4,834,114 |
| [Rescan-line STED](https://github.com/AndrewGYork/rescan_line_sted/tree/4a40942ec6237efaab873e8f7bcf4b81d7280b50) | 2 | 1 / 1 | 879,175 |

三个官方仓库的根`LICENSE`及README均明确将作品按 **CC BY 4.0** 发布。本轮只选择作者发表的光路原理、定制物镜和管镜工程图、装置机械线框及CAD渲染；保留完整论文作者表、图注与固定版本文章/附录来源。作者身份和作品许可来自原论文，不把GitHub托管者当作唯一作者。

14张管镜组件工程图分别具有明确的EFL焦距编号和不同组件结构，保留原编号；其余包括双倍/单倍远程重聚焦、单物镜光片扫描、多级成像光路及光学旋转切换。它们是具体研究设计的原图，应用到其他研究时应核对设计参数、保留作者及作品引用，不能把这些设计直接当作自己实验的装置说明。

大量实验结果曲线、显微成像数据帧、重复动画帧、设备照片、软件界面截图及包含第三方部件照片的拼图未收录。已发现的111张受激发射成像SVG主要是实验曲线、显微数据或照片，不因文件扩展名为SVG就全部当成通用插画入库。

29张位图全部完成Pillow `verify()`与完整`load()`解码、原生宽高、字节数和SHA-256复核；长边至少600像素且短边至少200像素。原生高清定义为长边至少1600像素，标准图长边600–1599像素，适合PPT中较小幅的示意图。三个源检出均为固定提交且工作区干净。

本地许可存档保留根README与LICENSE；图注与具体设计上下文通过固定提交的文章/附录链接追溯，没有将带上游JavaScript的HTML页面作为可执行站点内容镜像。

## 其他候选的处理

- NanaDraw是绘图软件，Bioicons素材与既有来源重复，其论文参考图画廊没有逐图再分发授权；软件采用附商业阈值的修改版Apache条款，未作为开放图库收录。
- Sciicons的GitHub仓库明确只有README，不存插画；README的CC BY 4.0不覆盖官网逐图素材。官网素材未实际取得，不计数量。
- ScanSci说明素材为AI辅助绘制，且没有覆盖全仓库的统一许可；具体物种形态与第三方参考权利仍需逐件核查，未因数量宣传批量导入。
- SCIY、HeroFig、Fig-Draw和Tesserax主要为绘图工具或生成器，未运行其代码并将输出伪装成上游原图。
- Xaviju的Inkscape符号库多为只有`defs/symbol`的整版，直接预览空白，未拆分成数百“上游原件”。其他缺少明确图像授权或来自既有电气源的图板未收。

各项统计只包含实际下载并核验的文件；未取得的网页素材、生成器代码、参考链接和格式派生物不计为新增原图。
