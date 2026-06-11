---
name: make-slides
description: >
  把论文 / 笔记 / 讨论变成一整套 villa 主题的 Beamer 幻灯片（中文 ctexbeamer）。
  当用户想"做 slide / 做组会报告 / 论文分享 / beamer 演讲 / 把某篇文章讲一讲"时使用。
  产出严谨、不溢出、风格统一、达到手工精排水准的 PDF。
---

# make-slides：论文/讨论 → villa Beamer 幻灯片

把源材料（论文、笔记、实验、和用户的思考）做成一整套 villa 主题 beamer 幻灯片。
本仓库**就是模版仓库**——用户每次复制它开新坑，所以这套 skill、工具、参考文档都随仓库一起带走。

## 核心理念：混合式（交互 + 确定性扇出）

按**“需不需要和人讨论”**切分阶段，而不是一把梭：

| 阶段 | 性质 | 谁来做 |
|---|---|---|
| **1 大纲设计** | 交互，最难，要反复和用户讨论 | 主对话 + 用户（**不要**派后台 agent，它没法和用户对话） |
| **1.5 公式校对** | 确定性 | 一个 agent / 小 workflow |
| **2 找图** | 确定性、可并发 | workflow 扇出，每图一个 agent |
| **3 逐页排版** | 确定性、可并发 | workflow 扇出，每页一个 agent |
| **4 合并终检** | 确定性 + 人复核 | 主对话（生成全文档、终检） |

> 为什么不全用一个 ultracode workflow：阶段 1 必须能和用户来回讨论，而 workflow 子 agent **中途无法向用户提问**。所以阶段 1 留在主对话里交互完成，2–3 才扇出。

## 脊柱契约：两个文件

整条流水线靠两个文件传递信息，别让后续阶段去"猜"：

- **`narrative.md`** — 这场报告的**组织主线**（一句话主旨、重组逻辑、关键洞见/分歧、刻意弱化、听众基调）。**以它为纲，原论文只作事实参考**，防止 agent 退回论文目录的流水结构。模版见 [`references/narrative-template.md`](references/narrative-template.md)。
- **`outline.yaml`** — 每一页的**完整内容**（标题、正文 markdown、**最终 LaTeX 公式**、图的规格）。schema 见 [`references/outline-schema.md`](references/outline-schema.md)。

阶段 1 产出这两个文件；1.5/2/3/4 都读它们。

## 五个阶段（playbook）

1. **大纲设计** → [`references/stage1-outline.md`](references/stage1-outline.md)
   和用户讨论出 `narrative.md`，再据此写满 `outline.yaml`（含完整公式、版式选择、图规格）。
2. **公式校对** → [`references/stage1.5-equations.md`](references/stage1.5-equations.md)
   抽取所有公式逐个编译，检查记号一致性。报告 + 安全修复。
3. **找图** → [`references/stage2-figures.md`](references/stage2-figures.md)
   按 `figures[].source` 并发找图：`tikz` 自己画 / `plot` 画数据 / `gpt_image` 生成 / `paper_crop` 截图 / `web` 搜 / `provided` 校验。**每个 agent 必须亲眼看渲染结果**。
4. **逐页排版** → [`references/stage3-typeset.md`](references/stage3-typeset.md)
   每页一个 agent：版式骨架 → 填内容 → **编译 → 渲染成位图 → 亲眼看 → 迭代**，直到不溢出且美观。
5. **合并终检** → [`references/stage4-merge.md`](references/stage4-merge.md)
   `tools/gen-slides.py` 拼装 `slides.tex`，xelatex 全量编译，逐页复核风格统一与连贯。

## 随仓库携带的工具链（已就绪、已实测）

- **`preamble.tex`** — 全场唯一的宏包/tikz 库/宏来源。`slides.tex` 和所有逐页/逐图 harness 都 `\input` 它，**保证“在 harness 里好看 == 在成品里好看”**。新增宏包只改这里。
- **`tools/buildframe.sh <id> "<section>"`** — 在隔离目录里用真实 preamble+villa(full) 编译 `frames/<id>.tex` 并渲染 PNG（150dpi），打印 PASS/FAIL + Overfull 警告。供排版 agent 的“编译→自看”循环。
- **`tools/buildtikz.sh <path.tikz.tex>`** — 把一张 tikz 图放到真实幻灯片上编译+渲染，供找图 agent 验收。
- **`tools/gen-image.sh <prompt> <out.png> [model] [size] [quality]`** — 调 GPT-Image-2/1 生成插图（OpenAI 兼容 relay，读 `.env`）。
- **`tools/gen-slides.py`** — 读 `outline.yaml` 拼出 `slides.tex`（section/subsection/帧顺序）。`uv run --with pyyaml python tools/gen-slides.py`。

**隔离原则**：每个并发 agent 用独立 build 目录（`.build/frames/<id>/`、`.build/tikz/<name>/`），靠 `TEXINPUTS=<repo>` 找仓库资源，不复制、不冲突。善用 git 在每个阶段后 commit 做备份。

## 编排建议

- 阶段 2、3 用 **Workflow 扇出**（每图/每页一个 agent），推荐 **scout-first**：先派 1 个 agent 把一类活儿（一张代表性图 / 一页密集帧）端到端打通并**返回经验 markdown**，把经验注入再铺开其余。这样既降风险又攒下可写进本 skill 的实战经验。
- 子 agent **有视觉**：让它们用 `Read` 打开渲染 PNG 亲眼比对 `must_show` / 检查溢出——这是质量的关键，别省。
- 收尾自己再 Read 一遍全图/全页的 contact sheet 复核，别只信 agent 的自述。

## 工具/环境约定（macOS）

这套 skill 在 macOS + Homebrew 上开发、实测。换一台 Mac 也能跑——装齐下面四样即可，**不需要**联网授权（除 GPT-Image 找图）。

### 需要的工具链

| 用途 | 命令 | 来自 | 怎么装 |
|---|---|---|---|
| LaTeX 引擎 + `latexmk` + `pdfcrop` | `xelatex` `latexmk` `pdfcrop` | MacTeX（`/Library/TeX/texbin`） | `brew install --cask mactex`（全量，省心；含 ctex/pgfplots/booktabs 等所有用到的包） |
| PDF→PNG 渲染、按 bbox 裁图 | `pdftoppm` `pdftocairo` | poppler | `brew install poppler` |
| 跑 python 工具（拼装/画图/拉数据） | `uv` | Homebrew | `brew install uv` |
| 解析 JSON（脚本里偶用） | `jq` | 系统自带 / Homebrew | macOS 自带；缺则 `brew install jq` |

一行装齐：`brew install --cask mactex && brew install poppler uv jq`。

- **轻量替代**：嫌 MacTeX 大（~5GB）可用 `brew install --cask basictex`，再 `sudo tlmgr install ctex pgfplots booktabs subcaption siunitx mathtools` 按需补包；新机器建议直接上全量 MacTeX 省去补包来回。
- **不需要 ImageMagick**：contact sheet 用 `uv run --with pillow` 的 PIL 拼，不依赖 `convert`。

### 关键约定

- **LaTeX 引擎只用 `xelatex`**（ctexbeamer 必需），全量编译跑两遍（解析目录/引用）。`latexmk -xelatex` 会自动跑够遍数。
- **中文字体零配置**：ctex 在 macOS 上自动挑系统 CJK 字体（苹方/宋体），**无需手动装字体或设 `fontset`**。换非 mac 系统才需显式配字体。
- **python 一律 `uv run --with <pkg> python …` 或 `uvx`，绝不全局 `pip install`**；常用包：`pyyaml`（拼装）、`pandas matplotlib seaborn`（画图）、`pillow`（拼图自看）、`trackio`/`gradio_client`（拉实验数据）。全局 CLI 工具走 `brew`。
- **GPT-Image 找图要联网 + key**：`tools/gen-image.sh` 读仓库根 `.env` 的 `OPENAI_BASE`/`OPENAI_KEY`（OpenAI 兼容 relay）。`.env` 必须在 `.gitignore` 里，别提交 key。该脚本只用系统 `python3` + urllib，无额外依赖。详见 [`references/gpt-image.md`](references/gpt-image.md)。

### 主题选项（建在 villa 之上）

- `\usetheme{villa}`：长报告 full（用 `\section` + 目录页，左上圈显示 section 名）。
- `\usetheme[nosection]{villa}`：短报告（≤10 页，无目录，左上圈显示帧标题）。
- `\usetheme[pku]{villa}`：纯北大 logo（去实验室 banner）。
- `\usetheme{uestc}`：UESTC 变体。

完整主题文档见仓库 `README.md`；模版长度对版面的影响见 [`references/layouts.md`](references/layouts.md) 的「模版长度」一节。

## 参考文档索引（`references/`）

- 规格类：[`outline-schema.md`](references/outline-schema.md) · [`layouts.md`](references/layouts.md) · [`math-density.md`](references/math-density.md) · [`report-structure.md`](references/report-structure.md) · [`data-sources.md`](references/data-sources.md) · [`narrative-template.md`](references/narrative-template.md) · [`gpt-image.md`](references/gpt-image.md)
- playbook 类：`stage1-outline.md` · `stage1.5-equations.md` · `stage2-figures.md` · `stage3-typeset.md` · `stage4-merge.md`
