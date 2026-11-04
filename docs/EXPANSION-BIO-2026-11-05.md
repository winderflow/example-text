# 生命科学新专题来源核验（2026-11-05）

本轮补充两个此前未收录的独立来源，共 **95张原图、29,320,642字节（约28.0 MiB）**：64张药理、营养护理与公共卫生位图，以及31张模式生物、人体和植物结构SVG。数量只指原件，不将渲染预览或既有图的格式转换重复计算为新图片。全站最终统计以重新生成的目录为准。

| 来源 | 原图数 | SVG | 原生高清位图 | 原生标准位图 | 原始字节 |
| --- | ---: | ---: | ---: | ---: | ---: |
| OpenStax 护理历史开放插画 | 64 | 0 | 28 | 36 | 15,779,412 |
| EMBL-EBI Expression Atlas Anatomogram | 31 | 31 | 0 | 0 | 13,541,230 |

## OpenStax护理：药理、营养与公共卫生

官方仓库为 [openstax/osbooks-nursing-external-bundle](https://github.com/openstax/osbooks-nursing-external-bundle)，包含《Pharmacology for Nurses》《Nutrition for Nurses》和《Population Health for Nurses》。只使用固定历史提交 [`f0124920c65609137effe2333dea327d1c77accc`](https://github.com/openstax/osbooks-nursing-external-bundle/tree/f0124920c65609137effe2333dea327d1c77accc) 的原文件。

该提交的根 `LICENSE` 明确为 **Attribution 4.0 International**，README和三个前言模块 `m00482`、`m00484`、`m00492` 均明确采用CC BY4.0，并要求保留艺术作品图注中的作者、来源和许可。三本书的collection元数据也指向CC BY4.0。上述证据与选中图片对应的CNXML章节随收录清单保留。

上游在2026-03-23的 [`80d61e847fa0f23fe83626e72ecaee50200511c7`](https://github.com/openstax/osbooks-nursing-external-bundle/commit/80d61e847fa0f23fe83626e72ecaee50200511c7) 改为CC BY-NC-SA4.0；本轮取其父提交，未下载新版图片并套用历史许可。作者记为OpenStax（Rice University），原图注中的出版社署名保留在caption字段。

固定版本422张被引用的原文件中，335张因存在尚未单独核实的第三方作品credit，或明确修改自已经收录的OpenStax解剖、生物学插画而未选；3张作者肖像/照片及4张低于尺寸门槛的图片也未选。初筛69张全部制作联系表逐图审查，再排除学术诚信装饰横幅、食物记录空表、处方文字表单、纯公式题图和药片照片5张，最终保留64张。

这些原图包括：营养与健康11张、临床药理与护理34张、公共卫生与流行病学19张，覆盖自由基、动脉粥样硬化、肺与支气管疾病、药代与药效、注射位置、神经递质、凝血机制、内分泌、生殖、感染链及流行病学模型。保留原生像素和全部图内标注；28张原生长边至少1600像素，36张标准图长边600–1599像素且短边至少200像素，未上采样。

全部64张再次执行Pillow `verify()`和完整`load()`，重新核对宽高、字节数与SHA-256。除与全站目录进行精确SHA去重外，还用256位差分哈希对扩充前2,976张原生位图做近似重复筛查，阈值为12位差异以内，未发现候选近重复。该近似检查是辅助排查，不作为图像著作权判断。

## EMBL-EBI Anatomogram：物种与组织结构SVG

官方仓库为 [ebi-gene-expression-group/anatomogram](https://github.com/ebi-gene-expression-group/anatomogram)，固定提交 [`9fcc37022cce1e2862692a5f5fbfb78572b87e67`](https://github.com/ebi-gene-expression-group/anatomogram/tree/9fcc37022cce1e2862692a5f5fbfb78572b87e67)。README的Licence章节明确区分：代码采用Apache2.0，**全部images、anatomograms和switcher icons采用CC BY4.0**；没有以软件许可证推定图像许可。

31张原始SVG来自 `src/svg/`，覆盖人类、鼠类和脑部、拟南芥、水稻、玉米、小麦、大麦、番茄、马铃薯、高粱，以及牛、鸡、猴、鱼、蛙、蜥蜴等模式生物。作者记为EMBL-EBI Expression Atlas contributors，并保留原图中的署名图标、许可链接和透明组织层。

**原件默认是灰色轮廓或结构线稿。** 用于上游交互高亮的组织层设为透明；本轮未修改颜色、显露全部器官或声称这些原件是完整彩色器官图。脑部、植物花部和全株等图中可见的结构保持原样，可在矢量编辑器中按许可调整并标明修改。

全部31张核对XML、SHA-256以及脚本、事件处理器和外部资源引用，均通过本库的被动SVG规则；用Inkscape逐张渲染并视觉检查联系表，均可显示。渲染文件只用于核验，没有作为额外新图片计数；与扩充前全站原图无相同SHA。

## 其他候选的排除依据

- `dbcls/togopics` 官方仓库只有上传Commons的脚本，没有图片原件；不以MIT代码许可覆盖远端图片。
- `rdinnager/phylopic-mini`、`stark1tty/phylopic-image-set` 只有下载或分析代码，原图与逐图许可仍在外部服务，未作为已下载图源。
- `rafeequemv1/sciicons-free-icons` 明确仓库无图；README的CC BY许可不代替独立网站图片的逐件条款。
- `Avi7ii/scidraw-gallery` 不是SciDraw.io官方原图库，主要聚合外部教程和示例图，未取得充分逐图许可。
- `Shannon4Science/NanaDraw` 包含已有Bioicons、draw.io及论文参考图，附有额外商业条件，不作为新的开放原图库导入。
- `Rimagination/scansci-svg` 的AI辅助物种图未经过分类学形态核验，且未确认每图统一许可，未计为已核验科研原图。
- `lmcai/Scientific_illustrations` 明确CC BY-NC-SA，不满足本库允许商业再分发的收录范围。
- `GeneMANIA/bio-icons` 根文件为LGPL，但11个SVG包含Noun Project第三方改编作品，原图的具体许可版本未充分核实，未据此新增。

公开GitHub仓库搜索返回429后停止重复检索；没有绕过当前环境对独立图片站点的网络限制。未取得的官网图片、只有代码的工具和不明确许可的候选不计入本轮95张。
