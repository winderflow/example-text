# Noto与Fluent科研彩色SVG来源核验

核验日期：2026-11-06。本批新增Noto和Fluent两套独立设计风格的彩色图形，各443张，共886张SVG。用于科研交流、实验流程和PPT中的对象示意；这些是风格化符号，不将其当作按比例绘制的解剖图或机制结论。

## 许可与原件

Noto来自Google官方`googlefonts/noto-emoji`固定提交，清单为[`noto-science.json`](../data/source-selections/noto-science.json)。图像的直接许可依据是**`2D/svg/LICENSE`中的Apache2.0声明**，不是当前根目录用于字体的OFL。原图像版权声明和完整Apache2.0文本均保留在[`licenses/noto-science/`](../licenses/noto-science/)。完整许可的公共副本在[`licenses/common/Apache-2.0.txt`](../licenses/common/Apache-2.0.txt)，构建时按锁文件中的SHA256复制，不修改原许可证文本。

Fluent来自Microsoft官方`microsoft/fluentui-emoji`固定提交，原图适用MIT，清单为[`fluent-science.json`](../data/source-selections/fluent-science.json)。每个主题只收一种Color默认版本，不把Flat、High Contrast、3D或肤色变体重复计数；原始名称、Unicode和关键词来自官方元数据。

两套图形都保留原始SVG字节及其真实源路径、作者机构、SHA256和许可证据。不会将两套不同作者的独立设计说成同一文件的格式转换，也不会将源文件的32/128等默认显示宽高标成位图原生像素分辨率。

## 收录和视觉检查

选择动物、植物、人体部位、实验设备、工程工具、计算图表、天气天文及数学/实验安全符号。排除情绪表情脸、旗帜、神话生物、游戏、货币和无关装饰。888张候选全部经过Chromium实际渲染、非空白检查和联系表视觉核对；额外从两套候选各排除1张Phoenix神话图形，最终886张。全部通过SVG脚本、事件、外部资源和原始SHA检查，与此前图库没有相同原始字节。

科研主题、逐图预览及下载见[本轮分类目录](MORE-OPEN-ART-2026-11-06.md)。图中的医疗或安全符号不额外授予商标、机构标识或受保护标志的使用权，具体用途仍参见[既有许可指南](LICENSES.md)。
