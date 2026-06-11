# 阶段 3：逐页排版（并发扇出）

每页一个 agent：取版式骨架 → 填 `outline.yaml` 的内容 → **编译 → 渲染成位图 → 亲眼看 → 迭代**，
直到不溢出且美观，达到手工精排的 beamer 质量。这是用户最看重 agent 帮忙的一步。

产出 `frames/<id>.tex`，**只含 `\begin{frame}...\end{frame}`**（无 preamble、无 `\section`）。
推荐 **scout-first**：先派 1 个 agent 排一页密集帧、返回经验，再注入铺开其余。

## 工作循环

1. 读 `outline.yaml` 里 id=该帧 的 frame；按 `layout` 去 [`layouts.md`](layouts.md) 取骨架（含容量上限）；body 约定见 [`outline-schema.md`](outline-schema.md)。
2. 写 `frames/<id>.tex`。
3. `bash tools/buildframe.sh <id> "<section>"`（仓库根目录，第二参数传真实 section 名以贴近最终左上圈效果）。
   - 打印 `PASS <id> pages=N` + PNG 路径 + 最多 5 条 Overfull/Underfull。**警告为空 = 没有静默溢出**，第一道体检。
   - 失败打印 log 尾 40 行，改完重跑。每个 id 独立 `.build/frames/<id>/`，可并发。
4. **用 `Read` 打开 `.build/frames/<id>/page-1.png` 亲眼看**（多页还有 page-2…）：溢出/裁切？标题一行放得下？图大小合适？密度舒服？像手排吗？警告干净 ≠ 布局好看。
5. 不满意就迭代到好。

## markdown→LaTeX 稳妥写法（实战）

- `$$...$$` → `\begin{equation*}...\end{equation*}`；带 `<!--label:eq:x-->` 的把 `\label{eq:x}` 放进 equation* **内部**（公式体后、`\end` 前）。
- 一个 display 里两段并排公式用 `\qquad` 分隔（loss + 条件均值），比拆两个更紧凑像手排。
- **`==X==` 必须翻成 `\alert{X}`，绝不能原样照抄**（照抄会渲染成字面 `==`，这是最常见的坑）。`\alert` 是 villa 主题红，适合放本页 insight 句 / 反问。
- `**X**`→`\textbf{X}`；`> 旁白：X`→`\narration{X}`（preamble 已定义：自成一行的等宽小字）。
- 中英混排（"条件 flow matching"、"paired data"）直接写，ctexbeamer+villa 处理得当，**不用手动加空格**。
- 公式防过宽：`\mathbb{E}_{...}\!\left[...\right]` 用 `\!` 收紧期望下标与括号间距；inline 分式可用 `\dfrac` 让它与正文同高更清晰；`→` 在数学语境写 `$\to$`。
- {{fig:ref}} → 按 figures[] 的 path：`.png/.pdf` 用 `\includegraphics[width=...]{path}`；`.tikz.tex` 用 `\resizebox{\textwidth}{!}{\input{path}}` 缩到列宽（自带文字标注的概念图通常**不必再加 `\caption`**，加了反冗余）。

## 控溢出 / 调密度

- `derivation_flow`、`bullet_points` 等默认**顶对齐**，内容少时下方自然留白——这是呼吸感，**别硬塞 `\vfill` 居中**（反而显飘）。
- 分段：区分"事实陈述"与"关键洞见"用 `\bigskip`，轻分隔用 `\medskip`/空行。
- **一栏放不下**（典型：text_fig_split 右栏 bullet 被裁到页脚、报 Overfull \vbox）：先把该栏/该页设 `\small`（或 `\footnotesize`），**同时精简措辞**（删"把/直接/当前模型"等冗余字、避免一句话最后一个字单独占一行）。优先精简，其次缩字号。
- 表格（table_centric）：长文本列用 `p{宽}` + `>{\raggedright\arraybackslash}`（左对齐，消除两端对齐的难看大空隙和 Underfull）；全表 `\footnotesize` + `\arraystretch{1.15}`；竖向 overfull 就调小 arraystretch / 间距 / 个别单元 `\scriptsize`。
- `big_figure` 文字多时：把那句话挪进标题/副标题，去掉 caption，让图最大化（由排版 agent 定）。
- 实在塞不下→拆两页（同文件两个 frame），但优先压一页。references 用 `\begin{frame}[allowframebreaks]{参考阅读}`。

## villa 主题坑

- full 模版左上圈显示 **section 名**；section 名 >8 字会撑破圈/挤标题栏（实测 ≤9 字勉强、4 字最佳）。帧标题在圈右侧，只需不超一行页宽。
- **进圈的标题（short 模版的帧标题、full 模版的 section 名）别用 ①②③ 等带圈数字/生僻符号**：圈用的标题字体可能没有这些字形，会被**静默丢弃**（实测 `产出①` 圈里只剩"产出"，两页撞名）。要编号就用中文「一/二」或「1/2」。
- 正文里**不要 `\usepackage`**——所有宏包只在 `preamble.tex` 加载（`\narration`、booktabs、subcaption、siunitx、tikz/pgfplots、amsmath/mathtools/bm 都已就绪）。
- TikZ 图里引用的 `villatheme`/`villaaccent` 颜色由主题 sty 提供，`\input` 进来即可用。
