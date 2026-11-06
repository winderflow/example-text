# 科研插画与 PowerPoint 使用指南

图库还提供4,197张可直接插入PPT的原始PNG/JPEG，使用“原始位图 PNG/JPG（全部）”筛选可查看。413张原生长边至少1600像素；其余3,784张明确标记标准尺寸，长边600–1599像素、短边至少200像素，适合较小幅的装置、分子、电路、光路和科学示意图。详情列出真实宽高；不要将标准图大幅放大后当作高清原件。新增图片按学科与来源整理在[最新下载索引](MORE-OPEN-ART-2026-11-06.md)。

优先选择图库中的 **PPT 高清 PNG** 筛选项。点击图片可下载原始 SVG，也可下载长边 2400 像素的配套 PNG；详情列出实际像素尺寸、作者、原始来源和许可证。

这些 PNG 是对已取得授权的原始 SVG 的忠实栅格化，保留长宽比，不是 AI 补绘或新创作；不把转换出的 PNG 再计为额外科研插画。纯矢量内容可按像素尺寸清晰输出；原图本来内嵌位图的部分仍受原始细节限制。

## 直接使用

- [按图名和学科查找全部高清 PNG](PPT-INDEX.md)：无需启动网页，在 GitHub 上就可按名称找到具体图片。
- [下载 PowerPoint 素材板](../downloads/ppt-illustrations.pptx)：72 张精选插画，每张是独立图片，可直接复制到自己的幻灯片；完整署名位于对应页的备注中。
- 新版 PowerPoint：选择“插入 → 图片 → 此设备”，导入 SVG 可保持矢量缩放；能否转换为可编辑形状取决于 Office 版本与图形结构。
- 各版本 PowerPoint：导入 PNG 最稳妥。透明部分会保留；原图自带白色或其他背景时，也会保留该背景。
- 标注“建议使用 PNG”的图形包含 Office 不易处理的 SVG 排版元素。使用配套 PNG 可避免文字、标签或图形丢失。

素材板内是 PNG 图片，不是可拆分编辑的 SVG；相应原始矢量文件仍在仓库中。需要整批下载时可在 GitHub 选择 **Code → Download ZIP**。

SVG若包含原作嵌入的位图，该部分仍受原始像素限制，不能只凭扩展名视为全部路径均可无限放大。

## 保留署名

下载图片后，在图库点击“复制署名文本”，保存作者、具体作品来源和许可版本。PPT 可将这些信息放在图下注释、备注或末尾致谢页。PNG 转换不取消原始图片的 CC BY、CC BY-SA 等条件；公开分享改编图形时仍需遵守相应条款。

## 本轮质量整理

本轮恢复 218 张此前被兼容性筛选误排除的 Bioicons 原图，包含 30 张 SwissBioPics 细胞插图及 157 张 DBCLS 图形。418 张高清 PNG 的选择由 `data/ppt-selection.json` 记录：其中 200 张从已有 Servier / DBCLS 图形按专题挑选，另 218 张对应恢复的原图。来源、像素尺寸、原文件与 PNG 的校验值分别记录在目录及 `data/ppt-renders.json`，原始 SVG 字节保持不变。

Wellcome、Wikimedia Commons、RCSB 以及 Togo 官网新增原件目前仍受运行环境网络策略限制；尚未下载的官网图片不计入上述数量。已从 Bioicons 获得的 Servier / DBCLS 图形按具体历史许可使用，不能据此声称镜像了这些官网的全部最新素材。

## 维护者重建

页面和成品图片无需安装依赖即可使用。只有重新生成 PNG 或 PPTX 时需要以下步骤：

```bash
python3 scripts/build_catalog.py --sources /tmp/science-art-sources
npm ci
npx playwright install chromium
node scripts/render_ppt_png.cjs
python3 scripts/build_catalog.py --sources /tmp/science-art-sources
pip install -r requirements-ppt.txt
python3 scripts/build_ppt_deck.py
python3 scripts/validate.py
```

渲染器默认两个并行任务，禁止原图脚本与外部网络请求，按原始 SVG 哈希验证缓存。生成记录保存输出像素尺寸与 PNG 校验值。重建时使用已有 checkout；不必额外创建 Git worktree。
