# 电子器件与专业工程SVG扩充核验

核验日期：2026-11-06。本批新增Fritzing的708张实验电子器件SVG，以及FreeCAD的269张专业工程SVG，共977张原件；原始字节、元数据和许可证据保留。

## Fritzing：708张电子器件与实验组件

官方仓库：[`fritzing/fritzing-parts`](https://github.com/fritzing/fritzing-parts)，唯一固定提交`27535f2fd02097be9bed229b75aa8e9be282a4a0`。根`LICENSE.txt`明确将全部graphics和documentation按CC BY-SA3.0发布，不是只给软件代码许可后推定图形开放。

选取独立breadboard-view原始SVG，覆盖传感器与测量、控制器和数据采集、显示读出、供电与能源、电子元件、电机执行器、开关编码器以及实验接线板。逐条从FZP器件元数据保留标题、贡献者和来源证据；真实器件型号保留，不将型号名称等同于独立品牌标识图。

从1365个被引用的独立breadboard文件中初筛1225张安全候选；再排59张仅换文字/参数的相同几何变体。1166张完成实际渲染并逐页检查15页联系表，最终保留708张、42,883,597字节。排除PCB焊盘、旧版本、icon复制、简单针脚原语、独立logo、许可例外、未审核foreignObject及外链依赖，不将PNG/PDF副本重复计数。

完整选择清单：[`fritzing-components.json`](../data/source-selections/fritzing-components.json)。修改后公开再分发图形需遵守相同方式共享要求；完整许可和逐器件FZP证据在[`licenses/fritzing-components/`](../licenses/fritzing-components/)。

## FreeCAD：269张工程、FEM与几何图形

官方仓库：[`FreeCAD/FreeCAD`](https://github.com/FreeCAD/FreeCAD)，固定提交`bff5ddb3ae5e681d7ec3760e5be44259f745c3a8`。只收逐SVG写明creator/contributor与rights的专业图形，覆盖机械、建筑管路、有限元、流体、机器人、测量和参数化几何。

268张原SVG的声明为**`FreeCAD LGPL2+`**，本合集明确选择随附根`LICENSE`提供的LGPL2.1作为允许的后续版本，目录记作`LGPL-2.1-or-later`；这不声称原SVG写了2.1，也不改写原声明。另1张原图明确CC BY-SA4.0，单独保留其许可。每条记录保存原版权声明；如果原图另列许可链接则原样保留，校验器与SVG实际RDF内容逐条比对，支持resource、about与Alt文本三种写法。49张原图仅列rights而没有许可网址，目录不补造“原链接”，仍提供本次适用许可网址与完整文本。

278张候选全部实际渲染并检查7页联系表，排9张重复或状态变体，最终269张、3,594,387字节。没有收通用菜单动作、品牌图标、指针及配色状态副本。

清单：[`freecad-science.json`](../data/source-selections/freecad-science.json)。原SVG本身为可编辑源文件，作者声明与完整LGPL全文位于[`licenses/freecad-science/`](../licenses/freecad-science/)。下载后修改或再分发时须按具体许可保留源文件、声明及许可条件；网站代码MIT不会替代这些条件。

本轮预览和逐图下载见[分类目录](MORE-OPEN-ART-2026-11-06.md)。
