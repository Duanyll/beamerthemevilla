# GPT-Image-2 使用指南（找图来源 `source: gpt_image`）

> 状态：完整版。下方 API schema 对齐 OpenAI 官方 imagegen skill
> （权威参考：`~/.codex/skills/.system/imagegen/references/image-api.md` 与 `cli.md`）。

## 一句话定位

意思丰富的插图/流程图首选之一；当 `web` / `plot` / `tikz` 反复搞不定时求助于它。
**唯一缺点是贵**——所以不要默认用它，能用 paper_crop/tikz/plot 解决的就别开。

## 能力与特性

- **几乎没有短板**：与传统图像模型不同，它**几乎不会把文字写错**。
- 内置一个 **GPT-4o**：世界知识偏旧，但**专门训练过平面设计审美**，版式排布通常很好看。
- **会自己补全内容**：描述模糊时，GPT-4o 会用自己的知识把文字/元素补上——这是双刃剑：
  既省事，也可能加进你不想要的字。**要精确控制文字时必须显式约束**（见模板）。
- **风格一致性很好**：给一个风格描述（"现代风格""扁平插画"等），整图风格统一。
- **能读伪代码/源码画流程图**：可直接把一段伪代码、甚至**一整个 Python 源文件**丢给它画成流程图。
- 版式它**自己会想**（且通常很好，因为专门训练过），也可以外部指定。

## 常用提示词模板（duanyll 惯用）

```
请你帮我制作一幅用于 PPT 的插图，白色背景，现代风格，展示下面给定的内容，
只包含我提供给你的文字（防止你自己加字）：

<这里直接给一小段 Markdown 格式的大纲 / 伪代码 / 源码>
```

- 「白色背景」→ 贴 beamer 白底不突兀。
- 「现代风格」可替换为任意风格描述，一致性好。
- 「只包含我提供的文字」这句是**防止 GPT-4o 自作主张加字**的关键。
- 正文给 **Markdown 大纲**最顺手；要流程图就给**伪代码/源码**。
- 想自己定版式就在提示词里加版式要求；不加则用它自带的（通常够好）。

## 何时选它

- 表达的意思**信息量大 / 概念抽象**，文字描述比画图省力。
- `web` 找不到合适的、`plot`/`tikz` 试了几轮仍不理想。
- 需要"一张好看的概念插画"而非精确数据图（数据图用 `plot`）。

## 验收（与其它来源一样，必须亲眼看）

- 文字是否**完全是给定内容**、没有被加字/改字（它很少错，但仍要核对）。
- 风格/配色是否贴合白底 PPT。
- 分辨率是否够清晰。
- 不达标：调整提示词（更明确的文字约束/版式要求）重试，或换来源。

## 调用方式（API schema）

本仓库用 `tools/gen-image.py <prompt-file> <out.png> [--model] [--size] [--quality]`——读 `.env` 的
`OPENAI_BASE`/`OPENAI_KEY`（OpenAI 兼容 relay），打 `/images/generations`，把返回的 `b64_json` 解码存盘。纯 `python3`（stdlib urllib），无额外依赖。
（官方 codex skill 的 `image_gen.py` 是另一条路：走 `OPENAI_API_KEY` + openai SDK，schema 同下。）

**端点**
- 生成：`POST /v1/images/generations`（`client.images.generate`）。
- 编辑/合成：`POST /v1/images/edits`（`client.images.edit`）——传 `image`（gpt-image-2 最多 16 张）+ 可选 `mask`，
  用来"在已有图上改一处""把几张图合成一张"。改图时在 prompt 里**重复"只改 X、保持 Y 不变"**减少漂移。

**模型**（都以 `gpt-image-` 开头）
| 模型 | 用途 |
|---|---|
| `gpt-image-2` | **默认**。质量最好、密集文字/图表强、图像输入恒高保真。做 PPT 插图就用它 |
| `gpt-image-1.5` | 需要**原生透明背景**时的回退（见下） |
| `gpt-image-1` / `-mini` | legacy / 便宜草稿 |

**参数**
- `prompt`、`model`、`n`(1–10)、`quality`(`low`/`medium`/`high`/`auto`)、`output_format`(`png` 默认 /`jpeg`/`webp`)、
  `output_compression`(0–100，仅 jpeg/webp)、`moderation`(`auto`/`low`)、`background`(`transparent`/`opaque`/`auto`)。
- `size`：gpt-image-2 支持 `auto` 或**任意 WxH**，需满足：最长边 ≤3840、长宽都是 **16 的倍数**、长短边比 ≤3:1、
  总像素 65.5万–829万（>2560×1440 实验性）。常用 `1024x1024`/`1536x1024`(横)/`1024x1536`(竖)/`2048x1152`/`3840x2160`/`auto`。
  legacy 模型只认 `1024x1024`/`1536x1024`/`1024x1536`/`auto`。
- **质量取舍**：草稿/缩略 `low`；**终图、密集文字、图表/示意图、高分辨率用 `medium`/`high`**（PPT 插图我们用 `high`）。
- **编辑专用**：`input_fidelity`(`low`/`high`)——**只对 gpt-image-1/1.5/-mini**，gpt-image-2 恒高保真**不要传**；`mask` 仅 edit。

**透明背景**：gpt-image-2 **不支持** API 的 `background=transparent`。要原生透明 → 用 `gpt-image-1.5` + `background=transparent` + `png/webp`；
或在 gpt-image-2 上画**纯色背景**再本地抠图。一般 PPT 插图用白底即可，不需要透明。

**返回 / 花费 / key 坑**
- 返回 `data[]`，每张取 `b64_json` 解码。
- 按 token 计费：high 1536×1024 ≈ 几千 image-token（一张几美分）；测试先用 `low`。慢，一张几分钟。
- **rate limit 比文本严**：并发别超 ~3，否则 429。
- key 排错（relay 实测）：`This token has no access to model X` = key 按模型授权（图像 key 调 chat 模型会这样，正常，直接用 gpt-image-2）；
  `Invalid token` = key 失效/写错，让用户更新 `.env`。探活：发个 `--max-time 14` 的小请求，**超时(在生成)=鉴权通过**。

**留档**：每张图的 prompt 存到 `<out>.prompt.txt`，可复现、可微调。
