# 阶段 2：找图（并发扇出）

按 `outline.yaml` 每个 `figures[]` 找/做一张图。**可并发**：每张图一个 agent。
推荐 **scout-first**：先派 1 个 agent 把某一类来源端到端打通、返回经验，再把经验注入铺开其余。

## 铁律（所有来源共用）

- **必须亲眼看产出**：agent 用 `Read` 打开渲染好的图，逐条核对该图的 `must_show`，检查清晰度、文字是否正确（尤其 web / gpt_image）、文字够不够大（尤其论文截图）。不达标就调策略或换来源——**编译/下载成功 ≠ 图对**。
- **独立工作目录**：每个 agent 用自己的 build 目录（`tools/buildtikz.sh` 已按图名隔离到 `.build/tikz/<name>/`），靠 `TEXINPUTS=<repo>` 找资源，互不冲突。
- 产出落到 `figures[].path`；`.tikz.tex` 是内联 tikz 源，`.png/.pdf` 是位图/矢量图。
- 收尾时编排者自己再 Read 一张 contact sheet 复核全部图。

---

## `tikz`：自己画概念/流程/关系图

产出**只含 `\begin{tikzpicture}...\end{tikzpicture}`** 的 `.tikz.tex`（不要 documentclass/frame/preamble），它会被 `\input` 进幻灯片。
验收：`bash tools/buildtikz.sh imgs/<name>.tikz.tex` → 读 `.build/tikz/<name>/page-1.png` 亲眼看。

**实战经验（来自打通后的总结）：**
- 引擎 XeLaTeX，中文直接写进节点，ctex 已处理，无需转义。
- **主题色直接用，别再 `\definecolor`**：`villatheme`（深砖红，结构/方框边/箭头）、`villaaccent`（亮红，点睛/强调）。浅底填充 `fill=villatheme!6`（很淡的米色）干净不抢戏。配色克制：villatheme + 黑灰 + villaaccent 点睛即可。
- **尺寸**：自然尺寸画到约宽 ≤11cm、高 ≤6.5cm（16:9 正文区）。横向略大于纵向，给标题/页脚留白；第一眼就看 PNG 竖向有没有顶页脚。
- 库已在 `preamble.tex` 加载（positioning, arrows.meta, calc, fit, backgrounds, shapes.geometric, shapes.misc, decorations.*），**图里别再 `\usetikzlibrary`**。
- 箭头统一 `>=Latex`。边标签用 `font=\scriptsize, inner sep=2pt, fill=white`——`fill=white` 关键，盖住底下的线避免文字被穿过。
- 对称/环形布局用**极坐标** `at (90:2.9)` 比 positioning 链省事（如五节点闭环用五边形顶点角 90/18/-54/234/162）。
- 节点内多行用 `\\[3pt]`（加竖向间距），**别用裸 `\\`**（在某些节点里报 "no line here to end"）。
- 用 `text=villaaccent`（而非把 villaaccent 当 fill）给文字上色，否则会渲染成红色实心块。
- 文字图（如"源图→目标图"示意）放不下真实照片时，用占位形状示意（圆=物体、矩形=背景），照样能讲清。

---

## `plot`：用 matplotlib/seaborn 画数据曲线

适合实验指标/示意曲线。**首选拉数据自己重画**（矢量、风格统一），而不是截 dashboard。
`uv run --with matplotlib --with seaborn --with pandas python <脚本>`。

- **把画图的 .py 代码存下来**（放 `tools/` 或图旁），图就可复现、可微调——别用一次性内联代码。本仓库范例：`tools/plot-example.py`（自带合成数据、`uv run` 即可跑通，照着改成你的数据源）。
- **同时导出 PDF + PNG**：`fig.savefig("x.pdf")`（矢量，**beamer 就插这个**，投影/放大都清晰）+ `fig.savefig("x.png", dpi=150)`（位图，给 agent 亲眼检查）。frame 里 `\includegraphics` 指向 `.pdf`。
- **用 seaborn 内置样式**：`sns.set_theme(style="whitegrid", context="talk")` 一行就干净统一；关键线用 villa 砖红 `#A5300F` 呼应主题。
- 数据源见 [`data-sources.md`](data-sources.md)：本地 CSV，或 trackio 实例（`uv run --with trackio` CLI / gradio_client 拉指标）。
- 典型 reward CSV 列：`step, rollout_reward_mean, rollout_reward_std, val_reward_mean, val_reward_std`；**val 列常稀疏**（每 ~20 步才记一个点），画 val 前 `dropna()`。
- 风格（已用过、好看）：rollout = 实线 + `fill_between(mean±std)` 浅色带；val = 实线 + 圆点（砖红）；标题 / `xlabel=step` / `ylabel=reward` / 图例。
- **matplotlib 默认无中文字体**：标题/轴标签用英文或 run 名，中文说明放 beamer 的 caption/正文，省去配字体。
- 亲眼看（PNG）：坐标范围合理、图例不挡线、字号在 slide 上够大。

---

## `gpt_image`：GPT-Image-2 生成插图（已实测可用）

能力远强于传统生成模型（内置 GPT-4o，会自动排版、**很少把文字写错**），适合：示意性插图、从伪代码/要点画流程图、需要"现代 PPT 插画感"的图。**慢**（一张几分钟）、**按 token 计费**，作为 web/plot/tikz 搞不定时的好选择。详见 [`gpt-image.md`](gpt-image.md)。

**调用（OpenAI 兼容 relay，读 `.env` 的 `OPENAI_BASE`/`OPENAI_KEY`）：**
```bash
python3 tools/gen-image.py <prompt-file> <out.png> [--model M] [--size S] [--quality Q]
#   --model    gpt-image-2(默认) | gpt-image-1.5(要原生透明时) | gpt-image-1
#   --size     1536x1024(默认,横) | 1024x1024 | 1024x1536 | 也可任意 WxH(见 gpt-image.md 约束)
#   --quality  high(默认) | medium | low(测试省钱)  —— 密集文字/图表/示意图用 medium~high
```
- 端点 `POST {OPENAI_BASE}/images/generations`（生成）；改/合成已有图用 `/images/edits`。返回 `b64_json`（脚本已解码存 PNG）。高质量 1536x1024 约几千 image-token（一张约几美分）。**完整 API schema 见 [`gpt-image.md`](gpt-image.md)**。
- **prompt 模版**（防它自己加字）：「请你帮我制作一幅用于 PPT 的插图，白色背景，现代风格，展示下面给定的内容，只包含我提供给你的文字：」+ Markdown 要点提纲。把 prompt 存到 `<out>.prompt.txt` 留档。
- **亲眼核文字**：GPT-Image 偶尔仍会加字/串字——Read PNG 逐字核对，只保留你给的文字。
- **key 排错**（重要）：
  - `Invalid token`（new_api_error）= key 失效/被禁/写错，让用户在 relay 后台确认或更新 `.env`。
  - `This token has no access to model X` = key 是**按模型授权**的（图像专用 key 调不了 chat 模型，正常）；直接用 `gpt-image-2/-1` 即可。
  - 探活技巧：发一个 `--max-time 14` 的小生成请求，**超时(=在生成)就说明鉴权通过**，秒回报错才是真失败。

---

## 其它来源（本 schema 也支持，按需）

- **`paper_crop`** 论文截原图：`pdftoppm`/`pdfcrop --bbox`/`pdftocairo` 定位裁剪；论文图缩到 slide 上常**字太小**，裁掉白边只留核心子图，亲眼确认够大够清晰。
- **`web`** 网上找现成图：搜索下载；**严格核**清晰度、文字准确、版权。
- **`provided`** 用户自备（如自己跑的实验截图）：**不去找**，只校验文件存在 + 质量达标；在 `figures[].path` 直接指向即可。
