# `outline.yaml` Schema

`outline.yaml` 是整条工作流的**脊柱契约**：阶段 1 产出它，阶段 1.5（公式校对）、阶段 2（找图）、
阶段 3（排版）、阶段 4（合并）都读它。设计原则：

- **内容写实**——每帧的文字、公式（最终 LaTeX）、图的规格都定下来，不留"讨论 X"这种虚条目。
- **角度/旁白是一等公民**——`subtitle`、`> 旁白`、`==高亮==` 把讨论中得到的洞见固化，防止排版阶段退回原文逻辑。
- **像素留给排版层**——`layout` 只选版式名 + `layout_hint` 给自然语言建议；左右划分、图宽、字号由阶段 3 定。

---

## 顶层结构

```yaml
deck:   { ... }      # 全局元信息
frames: [ ... ]      # 帧列表，按放映顺序
```

### `deck` 字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `title` | ✓ | 完整标题 |
| `short_title` | | 页脚短标题（`\title[...]`），默认取 `title` |
| `author` | ✓ | 如 `段宇乐` |
| `date` | | 默认 `\today` |
| `theme` | ✓ | `villa` \| `uestc` \| `pku`（纯北大无实验室 logo）|
| `template` | | `full`（默认，长报告，用 `\section`+目录）\| `short`（短报告，`[nosection]`、无目录、**帧标题进圈须 ≤8 字**）。详见 `layouts.md` 模版长度一节 |
| `audience` | ✓ | 自由文本，写清听众与预期前提。排版/找图 agent 据此把握深浅 |
| `math_density` | ✓ | `0` 概念为主 · `1` 关键式 · `2` 多式 · `3` 完整推导链。**每档带现成代表帧见 `math-density.md`** |
| `target_frames` | | 大致帧数，给阶段 1 控制篇幅 |
| `sections` | full 必填 | section 顺序数组（驱动 villa 目录页与左上角编号；**每个名 ≤8 汉字/20 字母，最好 4 字**）。论文分享类应覆盖 `report-structure.md` 的 8 点。short 模版省略 |
| `resources` | | 本场可用素材源（截图用 PDF、trackio 实例、主页等）。详见 `data-sources.md` |

### `frame` 字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✓ | 稳定唯一 id（kebab-case）。扇出时按 id 切分；图片文件名也建议带它 |
| `section` | full | 属于哪个 section（须在 `deck.sections` 中）。short 模版省略 |
| `subsection` | | 可空 |
| `title` | ✓ | 帧标题（勿超一行页宽；**short 模版下此标题进圈，须 ≤8 汉字/20 字母**）|
| `subtitle` | | **角度/洞见**，非小标签；可空 |
| `layout` | ✓ | 取自 `layouts.md` 的版式名 |
| `layout_hint` | | **自然语言**排版建议，如「左文右图，文字约六成」「下方最多 3 行」「图占满，文字放标题」；排版层参考，可偏离 |
| `reveal` | | `true` 表示该帧需分步（`\pause`/`\only`），节奏交排版层。默认 `false` |
| `body` | ✓ | markdown 块（见下），承载文字/公式/旁白/图占位 |
| `figures` | | 该帧用到的图的结构化规格列表（阶段 2 消费）。无图则省略 |

---

## `body` 的 markdown 约定

`body` 用 YAML 块标量 `|` 写 markdown。约定如下（排版 agent 据此翻成 LaTeX）：

| markdown 写法 | → LaTeX | 用途 |
|---|---|---|
| `$...$` / `$$...$$` | 同样的行内/行间公式 | **写最终 LaTeX**，排版 agent 照抄；放不下才简化 |
| `$$...$$` 后跟 `<!--label:eq:xxx-->` | `\label{eq:xxx}` | 需跨帧引用的公式打标签 |
| `- ` / `1. ` | `itemize` / `enumerate` | 列表（缩进表示嵌套）|
| `**粗体**` | `\textbf{...}` | 关键词 |
| `==高亮==` | `\alert{...}` | 行内高亮关键句 / 反问 |
| `> 旁白：...` | `\texttt{...}`（自成一行）| 口播过渡旁白 |
| `### 小标题` | `block` / 列定界 | 在并列版式里分隔并列槽（见下）|
| `{{fig:ref}}` | 对应图片的 `\includegraphics` | 图占位，`ref` 对应 `figures[].ref` |

**并列版式的槽位**：`parallel_blocks` / `image_grid` 这类有多个对等区域的版式，用 `### 标题`
分隔各槽（标题即 block 标题）。单一文字区 + 图的版式（`text_fig_split` 等）不需要分隔——
正文是文字、`{{fig:ref}}` 是图，排版 agent 自然分配。

> body 是给排版 agent 的"内容 + 意图"，不是最终布局。可以在 body 里用自然语言提示位置
> （"左栏放推导，右栏放 {{fig:xxx}}"），排版 agent 会参考但不被绑死。

---

## `figures[]` 字段（阶段 2 找图 agent 消费）

| 字段 | 必填 | 说明 |
|---|---|---|
| `ref` | ✓ | body 里 `{{fig:ref}}` 引用的名字，帧内唯一 |
| `path` | ✓ | 产出文件相对路径，建议 `imgs/<frame-id>-<ref>.png`（tikz 用 `.tikz.tex`）|
| `source` | ✓ | 见下方枚举 |
| `intent` | ✓ | 这张图**要表达什么**（找图 agent 的搜索/绘制目标）|
| `must_show` | ✓ | 图里**必须出现**的要素，找图 agent 的**验收清单**（亲眼核对）|
| `from` | | 来源线索：论文 `Fig.x`、网址、数据描述、参照图等 |
| `width` | | 宽度建议（相对所在列/页），排版层可调 |
| `status` | ✓ | `todo` → `done` / `failed`，阶段 2 回写 |

### `source` 枚举与各自的找图策略

| 值 | 含义 | 找图 agent 怎么做 |
|---|---|---|
| `paper_crop` | 论文 PDF 截原图 | PDF 工具定位+裁剪；**核对文字够大够清晰** |
| `web` | 网上找现成图 | 搜索下载；**核对清晰度、文字准确、版权** |
| `plot` | 自己用 matplotlib/seaborn/plotly 画 | 写脚本生成；适合数据曲线/示意 |
| `gpt_image` | GPT-Image-2 生成 | 见 `gpt-image.md`。意思丰富、或 web/plot/tikz 反复搞不定时用；贵 |
| `tikz` | 直接写 TikZ 画 | 写 tikzpicture，编译成 PDF/PNG 自看；适合关系/流程/概念图 |
| `provided` | 用户已自备/提前截好 | **不去找**，只校验文件存在 + 质量达标 |

无论哪种来源，找图 agent 都**必须把产出图渲染出来亲眼看一遍**，对照 `must_show` 验收；
不达标就调整策略或换来源。

---

## 完整示例

```yaml
deck:
  title: "Flow Matching 与 Diffusion 的联系与讨论"
  short_title: "Flow & Diffusion"
  author: "段宇乐"
  theme: villa
  template: full
  audience: "组会；听众已懂 diffusion 基础，想听推导与不同模型间的联系"
  math_density: 3
  target_frames: 30
  sections: ["理论框架", "联系与讨论", "参考阅读"]
  resources:
    papers:
      - {id: fm, path: refs/flow-matching.pdf, note: "FM 原论文，截图来源"}
    trackio: "http://192.168.5.133:7860/"

frames:
  - id: ddpm-bayes
    section: "理论框架"
    subsection: "DDPM 与 DDIM 回顾"
    title: "DDPM 的贝叶斯推导"
    subtitle: "一种推导 DDPM 的方式"
    layout: derivation_flow
    body: |
      定义前向过程
      $$x_t=\alpha_t x_{t-1}+\beta_t\epsilon_t,\quad x_t=\bar\alpha_t x_0+\bar\beta_t\bar\epsilon_t,\quad \alpha_t^2+\beta_t^2=1.$$ <!--label:eq:ddpm-forward-->
      为反向去噪求 $p(x_{t-1}\mid x_t)$，引入 $x_0$ 作条件写贝叶斯公式
      $$p(x_{t-1}\mid x_t,x_0)=\frac{p(x_t\mid x_{t-1})\,p(x_{t-1}\mid x_0)}{p(x_t\mid x_0)}.$$
      代入前向过程、按正态分布运算，得到含未知 $x_0$ 的分布。
      > 旁白：接下来训练网络预测噪声，就能消掉 $x_0$。

  - id: fm-path-choice
    section: "理论框架"
    subsection: "Flow Matching"
    title: "概率路径的具体选择"
    layout: parallel_blocks
    layout_hint: "左栏纵向并列两个 block，右栏放佐证图，文字约六成"
    body: |
      ### DDIM 速度场
      按 DDIM 参数设 $\mu_t,\sigma_t$，展开得复杂的 $u_t(x\mid x_1)$：
      $$\mu_t(x_1)=\bar\alpha_{1-t}x_1,\quad \sigma_t(x_1)=\sqrt{1-\bar\alpha_{1-t}}.$$

      ### OT 速度场
      $$\mu_t(x_1)=t\,x_1,\quad \sigma_t(x_1)=1-(1-\sigma_{\min})t.$$

      > 旁白：发现 ==OT 速度场收敛更快==，采样效果更好。

      右栏放 {{fig:checkerboard}} 佐证。
    figures:
      - ref: checkerboard
        path: imgs/fm-path-choice-checkerboard.png
        source: paper_crop
        from: "FM 论文 Fig.3 右"
        intent: "棋盘格数据上 OT vs DDIM 路径/采样对比"
        must_show: "棋盘格散点 + 两种方法的采样结果"
        width: "1.0"
        status: todo

  - id: derive-framework
    section: "联系与讨论"
    title: "推导 Flow 和 Diffusion 不同联系的理论框架"
    subtitle: ""
    layout: tikz_concept
    body: |
      四个对象两两相连构成关系图，见 {{fig:framework}}。
    figures:
      - ref: framework
        path: imgs/derive-framework.tikz.tex
        source: tikz
        intent: "OT/DDIM 速度场、DDIM ODE、DDPM SDE 四块及其转换关系"
        must_show: "四个带公式的方框 + 四条带标签的双向箭头(Affine Scaling / Reparameterization / Zero noise limit / Tweedie's Formula)"
        width: "0.8"
        status: todo

  - id: my-ablation
    section: "联系与讨论"
    title: "实验：过大的噪声尺度导致过平滑"
    layout: text_fig_split
    layout_hint: "左文右图，文字约 55%；左侧两条要点别超 4 行"
    body: |
      - 增大 $\sigma_t$ 没带来更多随机性，反而结果==过于集中==
      - $t\to1$ 时 Tweedie 公式发散 + 网络误差，可能是主因

      右图是我自己跑的对照实验 {{fig:ablation}}。
    figures:
      - ref: ablation
        path: imgs/my-ablation.png
        source: provided
        intent: "不同噪声尺度下生成结果的过平滑现象"
        must_show: "随 sigma 增大逐渐平滑的图像序列"
        status: todo
```
