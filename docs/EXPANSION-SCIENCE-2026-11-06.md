# 2026-11-06：物理与科学插画候选检索记录

本分支没有将未核清图像授权或没有现成图片文件的候选加入图片数量。下列结果是检索及排除审计，不代表已经镜像这些项目。

## PhET 官方素材：未导入

核查官方 [`phetsims/scenery-phet`](https://github.com/phetsims/scenery-phet) 固定提交 [`13a8f59bbd63c1d8aed1cfd9e9ddc73080117ec7`](https://github.com/phetsims/scenery-phet/tree/13a8f59bbd63c1d8aed1cfd9e9ddc73080117ec7)。根 `LICENSE` 是 MIT 软件许可，但同一版本的 [`images/license.json`](https://github.com/phetsims/scenery-phet/blob/13a8f59bbd63c1d8aed1cfd9e9ddc73080117ec7/images/license.json) 对实际仪器、滴管、水龙头、手部和橡皮等图像逐条标注 `contact phethelp@colorado.edu`。没有将代码 MIT 许可覆盖到另有逐图声明的图片。

同时检查历史提交 [`183e3c7af921b83f4bb4dabefb9bc829fd9a93cb`](https://github.com/phetsims/scenery-phet/blob/183e3c7af921b83f4bb4dabefb9bc829fd9a93cb/images/license.json)：当时的23条图像记录同样要求联系权利方，并未发现可据以再分发这些独立图片的历史 CC BY 声明。本次未导入这些资产，也没有从仿真界面截屏后当成原始素材。

## 其他候选

| 项目与固定版本 | 实际发现 | 本次处理 |
| --- | --- | --- |
| [`mrharksen/physics-diagrams`](https://github.com/mrharksen/physics-diagrams/tree/3cb61d13d0918dca3b4f071ddfa7f906df7e6fc0) | 70张物理SVG | 仓库未提供LICENSE，SVG中的Creative Commons XML命名空间本身不构成许可声明；未收录。 |
| [`nils-tomforde/feynman_diagrams`](https://github.com/nils-tomforde/feynman_diagrams/tree/53ff1ed95e3ee830af4bfebf78d1a3c41e03de70) | Python图形生成代码，没有已存SVG图片集 | 未运行代码生成图片，也未计入原图。 |
| [`syed-nazmus-sakib/PhysDraw`](https://github.com/syed-nazmus-sakib/PhysDraw/tree/3e14dd905cc04fe986314116b222b05e4c67139e) | 物理图形DSL及示例代码，没有已存图片集 | 未将工具或生成示例计作已下载图库。 |
| [`lightandmatter/lightandmatter`](https://github.com/lightandmatter/lightandmatter) | 检查时为空仓库 | 没有可下载原图，未计数。 |
| [`rdkit/rdkit`](https://github.com/rdkit/rdkit/tree/4d1e2824988b95688de222fd96f71b75a3e7ac80) | 当前树仅4张非品牌文档SVG，另2张为项目标志；并非预期的大量分子SVG回归图库 | 根BSD3软件许可已查；本次没有独立核清这4张文档图的具体作者与图像许可范围，不作图库导入。该结论不是断言RDKit输出图形不能使用。 |

已有缓存的York其余自包含论文也复查了实际文件：`stimulated_emission_imaging` 的大量SVG是显微结果、重复实验帧或实验装置照片；`relaxation_sensors`主要是实验图、曲线与参数扫描帧；`freeform_3d_optical_design`和`snoutscope`当前缓存没有可直接收录的独立图片集合。没有将这些内容按扩展名批量凑入通用科研插画数量。已入库的29张显微光学原理和机械图仍保留，见此前的[显微光学审核](EXPANSION-SVG-2026-11-05.md)。

以上检索只使用可访问的公开GitHub来源；没有绕过独立官网的网络限制，没有关闭TLS、许可或原件校验。实际新增图片以本轮总目录和catalog为准。
