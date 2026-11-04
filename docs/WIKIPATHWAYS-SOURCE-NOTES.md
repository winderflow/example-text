# WikiPathways完整通路SVG来源与抽样核验

核验日期：2026-11-05。本轮图源为WikiPathways官方组织的[`wikipathways-assets`](https://github.com/wikipathways/wikipathways-assets)仓库，唯一固定版本为[`b171290fc3937590b673a602a71781ae4afa57fc`](https://github.com/wikipathways/wikipathways-assets/tree/b171290fc3937590b673a602a71781ae4afa57fc)。实际入库范围以来源选择清单与全站catalog为准；本次核验覆盖该版本的2,219张完整通路SVG。

## 许可范围

同一提交的[根LICENSE](https://github.com/wikipathways/wikipathways-assets/blob/b171290fc3937590b673a602a71781ae4afa57fc/LICENSE)为**CC0 1.0 Universal**完整文本。[README](https://github.com/wikipathways/wikipathways-assets/blob/b171290fc3937590b673a602a71781ae4afa57fc/README.md)说明此仓库保存“Accessory files generated downstream of approved GPMLs”。本次取得的SVG正是`pathways/WP编号/`中的正式图形资产，许可范围并非仅依据另一个网站的软件代码推定。

图形按该官方资产仓库的CC0发布声明收录。即使CC0不强制著作权署名，科研使用仍应保留WikiPathways编号、原编辑者、物种、修订版本和作品链接，以便读者追溯原图及相应科学文献。

完整SVG原文件逐字节保留；没有移除文字、箭头、作品编号或引用标记。根许可和README随来源保留。对该固定版本的全部2,219张SVG检查，未发现位图`image`节点、活动脚本或外部图像依赖，也未发现图内另列copyright、CC BY或其他第三方图像许可例外。

## 标题、编辑者和修订版本

每个SVG有同名JSON；JSON的`pathway`对象提供：

| 原字段 | 记录含义 |
| --- | --- |
| `name` / `displayName` | 通路名称，使用上游真实标题 |
| `organism` | 适用物种；不能将不同物种的同名通路合并成一幅人类通路 |
| `author` | 上游编辑者/贡献者列表，常为WikiPathways账户名，包含维护机器人；不是推测的个人画师姓名 |
| `dataSourceVersion` | 例如`WP999_r140474`，保留实际修订标识 |
| `lastModified` | 上游记录的最近编辑时间；不等于本库下载时间或所有知识更新至该日期 |
| `id` | 通常为WP编号；个别使用相同WP编号的canonical URI，需按编号一致性核对 |

`WP4153`的原始`author`是空列表；目录明确记为WikiPathways贡献者且“未记录个人作者”，没有补造姓名。其余原作者列表照录，完整元数据可由固定JSON链接核对。

WP5343的JSON `id`采用`http://identifiers.org/wikipathways/WP5343`，与文件名和修订标识`WP5343_r126461`对应；这是同一WP编号的URI表示，不另算第二张图。

来源记录保留原始JSON的固定版本URL和SHA-256，便于核对完整注释、科学来源和同源推断说明。目录采用图名、物种和修订信息，不镜像408MB的几何JSON，也不将第三方长篇描述复制后套用图像的CC0许可。

部分JSON科学描述引用Wikipedia、KEGG、BioCarta或相关文献，也有同源映射产生的物种通路。科学知识来源引用不自动等于复制了第三方图片；本次没有发现SVG内嵌入这些平台的位图或另列图像版权声明。第三方叙述文字的许可仍应按原始来源判断，官方资产仓库的CC0不用于重新授权这些外部文章。完整原注释留在可追溯的上游JSON中。

## 独立静态渲染抽查

在禁止外部网络请求的条件下，使用Chromium通过临时本地HTTP读取原始SVG，完成**18幅、9个物种**的真实浏览器渲染；包括文件体积最小和最大的图，全部成功解码、显示，零页面脚本错误。逐张查看渲染联系表，文字标签、反应箭头、分子名称与通路分区均可见。抽查包括：

| 编号 | 通路 | 物种 |
| --- | --- | --- |
| WP1027 | Glycolysis and gluconeogenesis | Bos taurus |
| WP1227 | TCA cycle | Anopheles gambiae |
| WP4946 | Genes and complexes involved in the DNA repair pathways | Homo sapiens |
| WP1018 | Apoptosis | Bos taurus |
| WP1050 | Oxidative stress response | Bos taurus |
| WP2233 | Immune responses in the epidermis | Caenorhabditis elegans |
| WP1461 | Photosynthetic carbon reduction | Arabidopsis thaliana |
| WP1008 | Amino acid conjugation of benzoic acid | Bos taurus |
| WP1043 | Calcium regulation in cardiac cell | Bos taurus |
| WP1401 | Neurotransmitter release in cholinergic motor neurons | Caenorhabditis elegans |
| WP1589 | Folate-alcohol and cancer pathway hypotheses | Homo sapiens |
| WP4863 | Host-pathogen interaction of human coronaviruses - autophagy | Homo sapiens |
| WP5653 | Kidney toxicity induced by activation of 5HT2C | Homo sapiens |
| WP1266 | SIDS susceptibility pathways | Mus musculus |
| WP1 | Statin pathway | Mus musculus |
| WP1329 | Alpha 6 beta 4 integrin signaling | Danio rerio |
| WP220 | Salvage pathways of pyrimidine deoxyribonucleotides | Saccharomyces cerevisiae |
| WP2886 | Acetaminophen synthesis | Escherichia coli |

SVG根节点常使用800×600作为默认显示尺寸，而实际`viewBox`因通路布局而异；这不是800×600像素位图，也不应据此称为低分辨率原件。完整通路包含大量小标签，适合放大查看和按需排版，不能保证把复杂网络缩在一页PPT上仍可读清每个基因名称。

本轮验证了静态浏览器显示，没有逐图在PowerPoint实机测试，不保证所有Office版本都能将每个元素拆分编辑。SVG是固定版本的通路图与科研制图素材，不是最新通路机制或研究结论的保证；用于发表前应结合物种、上游修订及科学文献核对。
