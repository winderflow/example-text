# 高清科研图片与 PPT 素材核验（2026-11-03）

本轮按用户指定的 Bioicons、Servier、Togo Picture Gallery、Wellcome、Wikimedia Commons 和 RCSB 方向，优先检查精细科研插画及高清原图。以下首先记录 Bioicons / Servier / Togo 的实测结果；实际入库数量与格式以 `data/catalog.json` 为准，不能把列出网址视为已下载。

## Bioicons：恢复此前技术筛选误排的精细原图

固定上游版本为 [`d29e766ea7580b8063c4f47b29e872db40a4d979`](https://github.com/duerrsimon/bioicons/tree/d29e766ea7580b8063c4f47b29e872db40a4d979)。本轮只读 `git ls-remote` 检查得到的 HEAD 仍是这个版本，**没有声称上游新增了图形，也没有把恢复文件计作另一个新素材库**。

首轮 229 个排除项重新逐文件核验后，有 218 个原始 SVG 可恢复：

| 类型 | 文件数 | 复核结论与使用方式 |
| --- | ---: | --- |
| 普通 SVG | 56 | 原始 SVG 无须改动。包括 30 张 SwissBioPics 精细细胞插图，以及实验器材、遗传与细胞相关图形。 |
| 含静态 `foreignObject` 的 SVG | 162 | 包含 157 张 DBCLS 插图。主要是 Drawio 导出的静态 HTML 文字标签；经逐文件检查没有脚本、真实事件处理器或外部图像依赖。保留 SVG 原文件，并提供 PNG 预览与 PowerPoint 兼容版本，避免 Office 对 `foreignObject` 的支持差异造成文字遗漏。 |

这 218 个文件原始 SVG 合计约 121.1 MB，数量代表文件，不代表 218 种全新科学概念。原图作者、原许可及固定版本链接须逐图保留，不改变 CC0、CC BY、CC BY-SA 等原有条款。

此前筛选过严的具体原因：

- 23 个文件中存在 `only_selected` 属性。它是编辑器设置，不是 `onload` / `onclick` 等事件处理器，不能仅因属性以 `on` 开头就判定为活动内容。
- SwissBioPics 部分 `<a href>` 是作者、来源或许可的普通链接，不是加载外部图片；在作为图像预览时也不是外部图像依赖。
- `color-profile` 中的 `data:application/vnd.iccprofile` 是内嵌色彩配置，不是远程资源。
- `foreignObject` 需要检查实际子元素、事件、脚本、样式与资源引用，不能把静态文字统一视为脚本。原始 SVG 仍可能与 PPT 的 SVG 支持范围不同，因此应配 PNG 版本。

对静态 `foreignObject` 的放行采用固定路径及原文件 SHA-256 核验，不是放开任意新 SVG。浏览器生成兼容预览时，应禁止额外网络请求并保留原图长宽比；增加像素尺寸不等于增加原始科学细节。

以下 11 个文件继续排除：3 个原本主动排除的软件品牌图标；4 个空白或 XML 结构损坏的文件；2 个含 mesh-gradient JavaScript polyfill 的文件；2 个引用缺失相对 JPG 文件的 SVG。没有删除脚本或补造缺失图片后再宣称“原图未修改”。

## Servier：现有具体图形的授权与官网边界

现有 Bioicons 子集中署名 Servier 的原图继续按其记录的历史 CC BY 3.0 授权保存。本轮访问 `smart.servier.com` 遭运行环境网络代理明确拒绝（403），因此没有把 Servier 官网全站的新图片或现行条款写成已经核验，也没有绕过网站或代理限制。

引用 Bioicons 中的 Servier 图形仍应署名 Servier Medical Art，提供原图来源及对应许可链接；公开部署这个合集不能替代使用者在论文和 PPT 中的署名义务。

## Togo：已核实官方数据与高清下载路径

DBCLS 官方仓库 [`dbcls/togotv`](https://github.com/dbcls/togotv/tree/ce0bf4e7f473d06d51c955ade7dddd856e0370bb)（本次核验提交 `ce0bf4e7f473d06d51c955ade7dddd856e0370bb`）的画廊源码提供以下公开入口：

- 元数据：`https://togotv-api.dbcls.jp/api/entries?target=pictures&rows=10000`。
- 原图主机：`https://dbarchive.biosciencedbc.jp/data/togo-pic/image/`，拼接元数据中的 `svg`、`png`、`ai` 等真实文件名。
- 元数据字段包括英文名、学名、作者、编辑、DOI、分类与文件名。官方 `_picture.vue` 同时提供 Wikimedia Commons 对应文件链接，并在 JSON-LD 中声明 CC BY 4.0。
- 部分作品另提供单色 SVG / PNG、细节图、动画或三维文件；不能猜文件名，也不能用缩略图尺寸冒充高清原件。

官方源码中的证据位置是 [`pages/_picture.vue`](https://github.com/dbcls/togotv/blob/ce0bf4e7f473d06d51c955ade7dddd856e0370bb/pages/_picture.vue)、[`components/DownloadModal.vue`](https://github.com/dbcls/togotv/blob/ce0bf4e7f473d06d51c955ade7dddd856e0370bb/components/DownloadModal.vue) 和 [`nuxt.config.js`](https://github.com/dbcls/togotv/blob/ce0bf4e7f473d06d51c955ade7dddd856e0370bb/nuxt.config.js)。画廊代码能确认官方接口和文件组织方式；新作品实际下载时仍需读取具体元数据并保存作者、许可和来源。

本轮直接访问 `togotv.dbcls.jp`、`togotv-api.dbcls.jp` 和 `dbarchive.biosciencedbc.jp` 均得到网络代理 403。已从 Bioicons 获得且本次可恢复的 DBCLS 图形可按原有逐图许可处理；这些结果**不等同于已经下载 Togo 官方完整画廊或其所有高清 PNG / AI**。

## PowerPoint 使用建议

- 新版 PowerPoint 可通过“插入 → 图片”导入 SVG；普通 SVG 可保持矢量缩放，是否可拆分编辑取决于 Office 版本及图形结构。
- 含 HTML 文字、复杂滤镜或其他 Office 不支持结构的 SVG，优先使用配套 PNG，以保留文字和效果；PNG 不再是可拆分编辑的矢量文件。
- 高清位图应记录原始像素尺寸。透明 PNG 适合与幻灯片背景叠放；历史扫描图和照片通常保留其原有背景，不应无依据地称为透明素材。
- PPT 中保留作者、来源及许可记录；CC BY-SA 图形发布改编内容时，还应遵守相同方式共享条件。
