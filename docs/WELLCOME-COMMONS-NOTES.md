# Wellcome 与 Wikimedia Commons 高清原图采集准备

核验日期：2026-11-03。本轮已准备许可核验与下载工具；**当前尚未从这两个站点下载或加入新的图片**。不能把工具自检、API 文档或空清单计为已收录素材。

## 当前访问情况

运行环境的 HTTP 网络策略处于 restricted / enforced。对下列官方域名的真实 HTTPS 请求均得到代理 `CONNECT 403 Forbidden`：

- `wellcomecollection.org`
- `api.wellcomecollection.org`
- `iiif.wellcomecollection.org`
- `commons.wikimedia.org`
- `upload.wikimedia.org`

这是当前执行环境的访问限制，不表示这些网站失效或要求登录。保存网络配置草稿并不会自动把新规则应用到正在运行的机器；应在规则实际应用后再重试。工具保留继承的代理与 TLS 校验，不更换域名或关闭校验绕过限制。

Wellcome 的官方开发者仓库可访问，但其中的开发文档、网站图标和代码截图不是用户所需的高清医学插画，未用它们充当新增图片。

## 许可核验依据

- [Wellcome 官方 Catalogue API 文档](https://github.com/wellcomecollection/developers.wellcomecollection.org/blob/main/reference/catalogue.yaml)：每个 image 的 `locations[].license` 才是图像位置对应的许可；`source.contributors` 提供作品贡献者，`locations[].credit` 提供署名信息。不能将目录数据的 CC0 自动套用于图片。
- [Wellcome 官方 IIIF 使用示例](https://github.com/wellcomecollection/developers.wellcomecollection.org/blob/main/docs/examples/03-connecting-the-apis-together.md)：`thumbnail.url` 指向 IIIF `info.json`，其中给出原始像素尺寸与图像服务地址。
- Wikimedia Commons 通过官方 MediaWiki API 查询每个文件的 `imageinfo` 与 `extmetadata`，保留 `Artist`、`Credit`、`LicenseUrl`、`LicenseShortName`、`Copyrighted` 和原始文件页；不能把 Wikimedia 的软件或网站文字许可套给上传图片。

采集器只接受明确的 CC0、CC BY、CC BY-SA 或公有领域标记。带 NC、ND、缺少明确图像许可、缺少必需署名、或提示需要另查限制的文件会排除。Commons 的公有领域判断要求文件元数据同时明确写出 `Public domain` 与 `Copyrighted=False`，且保存原始证据。所有许可版本均从具体文件信息读取，不统一改写成 4.0。

## 获取方式与质量

工具为 [`scripts/collect_web_images.py`](../scripts/collect_web_images.py)，只用 Python 标准库，不运行上游网站代码：

```bash
python3 scripts/collect_web_images.py --self-test

# 网络规则实际应用后执行；每个来源最多 150 张、120 MiB。
python3 scripts/collect_web_images.py --source both --limit 150 --max-mb 120

# 可单独收集指定研究方向。
python3 scripts/collect_web_images.py --source wellcome --query "anatomy engraving" --limit 80
python3 scripts/collect_web_images.py --source commons --query "cell biology diagram filetype:svg" --limit 80
```

默认结果保存在 `.cache/web-images/<source>/`，与已经发布的图库分开；不会自动修改图库目录或虚增网页计数。

- Commons 保存原始 SVG、PNG 或 JPEG 文件，不把缩略图冒充原图。
- 位图要求长边至少 1,600 像素；单文件限 15 MiB。
- Wellcome 从官方 IIIF 服务取得完整画面 JPEG，长边最高 3,200 像素，不放大低分辨率原图。清单会明确写为官方高清缩放版本，不称为未经处理的原始扫描件。
- 每图保存来源页、下载地址、作者、许可、像素、格式、文件大小、SHA-256、署名文本和 API 原始证据。
- 透明 SVG 的活动内容、脚本、事件处理与外部依赖会被排除，避免直接把活动网页内容作为可组合绘图素材。
- 默认每次请求间隔 0.3 秒、每个查询最多 3 页；遇到 403 立即停止，不反复重试被禁止的目的地。累计体积达到上限也会停止。

清单顶层包含 `source_id`、`assets`、`rejected` 和 `downloaded_bytes`；成功素材记录包含 `path`、`relative_path`、`source_url`、`download_url`、`author`、`credit`、`license`、`license_url`、`width`、`height`、`sha256`、`attribution` 和对应的 `evidence` 文件。后续核验与整理后，再由图库导入流程收录。

## 当前验证结果

`--self-test` 与 Python 编译检查通过。自检真实覆盖：从图片位置读取许可而非目录许可、拒绝 NC/ND、按 Commons 文件元数据保留作者、拒绝需人工复核的额外限制、读取 PNG 尺寸，以及正确生成不放大的 IIIF 高清请求。这些是本地构造数据的测试，**不表示远程接口与图片下载已经可用**。
