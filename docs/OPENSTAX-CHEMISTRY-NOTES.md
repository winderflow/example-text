# OpenStax 化学高清插图来源核验

核验日期：2026-11-04。此来源增加 2 张未经转换、裁剪或上采样的原始 JPEG：原子轨道形状，以及七大晶系与十四种晶胞。

## 版本与许可

- 官方仓库：<https://github.com/openstax/osbooks-chemistry-bundle>，教材为《Chemistry 2e》和《Chemistry: Atoms First 2e》。
- 唯一来源版本：[`32c719622fbb7a0ca729cd645c1df4cf4e7d5b3a`](https://github.com/openstax/osbooks-chemistry-bundle/tree/32c719622fbb7a0ca729cd645c1df4cf4e7d5b3a)。
- 该版本的 [LICENSE](https://github.com/openstax/osbooks-chemistry-bundle/blob/32c719622fbb7a0ca729cd645c1df4cf4e7d5b3a/LICENSE) 首行为 **Attribution 4.0 International**；[README](https://github.com/openstax/osbooks-chemistry-bundle/blob/32c719622fbb7a0ca729cd645c1df4cf4e7d5b3a/README.md) 将教材明确按 Creative Commons Attribution 发布。
- [教材集合元数据](https://github.com/openstax/osbooks-chemistry-bundle/blob/32c719622fbb7a0ca729cd645c1df4cf4e7d5b3a/collections/chemistry-2e.collection.xml) 明确链接 CC BY 4.0；[前言模块](https://github.com/openstax/osbooks-chemistry-bundle/blob/32c719622fbb7a0ca729cd645c1df4cf4e7d5b3a/modules/m68662/index.cnxml) 明确允许分发、改编，要求署名 OpenStax 及其内容贡献者。

2026-03-19 的上游提交 [`0243cd5879b93936ad8bc70ca181480403c331ec`](https://github.com/openstax/osbooks-chemistry-bundle/commit/0243cd5879b93936ad8bc70ca181480403c331ec) 将许可改为 CC BY-NC-SA。当前主分支不是此次图源；更新时不能从新版本取图并套用历史许可。

## 实际选择与限制

清单：[`data/source-selections/openstax-chemistry.json`](../data/source-selections/openstax-chemistry.json)。

- 2 张原始 JPEG，共 **1,132,747 字节**；原始尺寸分别为 **1300 × 1600** 和 **1297 × 1600**。
- 每张已完整校验 JPEG 解码、尺寸、SHA-256，并与已有图库进行字节去重；文件本身没有改动。
- 两图所在 CNXML 图形节点未出现外部第三方署名、courtesy 或修改外部作品等例外；来源证据模块分别是 `modules/m68733/index.cnxml` 和 `modules/m68773/index.cnxml`。
- 全仓库 1,536 张常规图片中只有 3 张原始长边达到 1600 像素；另 1 张为带外部署名的星云照片，已排除。其余图片多数为 600–1300 像素，本轮未将其上采样后计作高清素材。
- 官方 `osbooks-organic-chemistry` 的 LICENSE 自 2022 年即为 CC BY-NC-SA，不在本次可自由再分发来源中。

使用时保留 OpenStax (Rice University)、教材来源及 CC BY 4.0 许可信息；修改图片应说明修改。JPEG 可直接插入 PowerPoint，属于原生高清位图。
