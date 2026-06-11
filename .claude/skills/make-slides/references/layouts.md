# 版式目录 (LAYOUTS)

这是 **outline agent** 和 **排版 agent** 共享的版式菜单——一份覆盖学术报告常见场景的版式清单，
每个都给了可直接套用的 LaTeX 骨架与（16:9、villa 默认字号下的）容量上限。

- **outline agent** 在 `outline.yaml` 的 `layout:` 字段里**选一个下面的名字**，并在
  `layout_hint:` 里用**自然语言**给排版建议（如「左文右图，文字约占六成」「上图下文，下面最多三行字」）。
  它只负责挑版式、组织内容，**不写死像素**。
- **排版 agent** 拿 `layout` 名 → 取下面对应的 LaTeX 骨架 → 填入 `body` 内容 → 编译渲染自看。
  比例、图宽、字号都可以为了美观和不溢出而**偏离建议值**；甚至在内容明显不适配时换一个更合适的版式
  （换之前在该帧 `body` 末尾留一行 `> 排版备注：原 layout=X，改用 Y，因为……`）。

## 通用约定（所有版式共用）

```latex
\begin{frame}{帧标题}{副标题（可空，承载本页角度/洞见）}
  ... 内容 ...
\end{frame}
```

- 帧标题**别超过一行页宽**，否则 villa 的标题栏排版会乱。
- 公式中的文字用 `\mathrm{}`/`\text{}` 包住（`\mathrm{clip}` 而非 `clip`）。
- 矢量图优先 `.pdf`，位图用 `.png`；宽度用 `\textwidth`/`\columnwidth` 的分数。
- 需要逐步显示时加 overlay（见末尾「叠加维度 · reveal」）。
- **塞进左上角圈里的文字必须 ≤8 汉字 / 20 字母（最好 4 字）**，否则圈被撑破、标题栏错位（详见下「模版长度」）。

**关于「文字容量」**：下面每种版式给的行数是 **16:9、villa 主题、默认字号**下的粗略上限。
排版 agent 可用 `\small`/`\footnotesize` 再挤入约 30~50%，但应**优先精简措辞**而非一味缩字号；
超出容量就拆页、精简、或换版式。一「行」按页宽（或所在栏宽）排满一行的中文计。

---

## 模版长度：full / short

deck 有两种模版（`outline.yaml` 的 `template` 字段），**section 用法与"什么进圈"完全不同**：

| | full（默认，长报告） | short（短报告） |
|---|---|---|
| 引入 | `\usetheme{villa}` | `\usetheme[nosection]{villa}` |
| 章节 | 用 `\section`/`\subsection` | **不用 section** |
| 目录页 | 开头一页 + 每节自动插 | 无 |
| 左上圈内 | 当前 **section 名** | **本页帧标题** |
| 左上徽章 | section 编号 | 页码 |
| 帧标题位置 | 圈右侧（只需不超页宽）| 进圈（须很短）|
| 适合 | 论文分享(8 点)、深入报告 | ≤10 页快速分享 |

**标题长度硬约束**：进圈的文字 **≤8 汉字 / 20 字母，最好 4 字**——
- **full**：约束 **section 名**（帧标题在圈外，只需不超一行页宽）。
  例：8 点 section 名「论文信息 / 任务背景 / 已有方案 / 研究动机 / 观察启发 / 提出方法 / 实验对比 / 个人评价」都是 4 字，正好。
- **short**：约束**每个帧标题**（它进圈）——起标题时就压到 ≤8 字。

---

## A. 文字流版式

### `derivation_flow` 满页推导
**何时用**：深推导页，一串公式靠散文串起来（"代入…得到…替换…得到"）。组会/深入向的主力。
**默认比例**：单栏。
**文字容量**：约 12~14 行等价高度；每个 display 公式约占 3 行，故 **≤3~4 个公式 + 连接散文**。
```latex
\begin{frame}{标题}
  引子散文，引出第一个式子
  \begin{equation*}
    ...
    \label{eq:xxx}
  \end{equation*}
  过渡散文（"代入上式得到"）
  \begin{equation*} ... \end{equation*}
  收尾一句结论 / \alert{关键含义} / 旁白
\end{frame}
```
**注意**：放不下时拆页或把中间步骤简化。

### `bullet_points` 要点列表
**何时用**：贡献、背景、takeaways、小结。
**默认比例**：单栏。
**文字容量**：约 **6~8 个一级条目**（每条 1 行），或 ~10~12 行正文；带两级嵌套则相应减半。
```latex
\begin{frame}{标题}
  一两句引子散文。
  \begin{itemize}
    \item 要点
      \begin{itemize}\item 次级要点\end{itemize}
    \item 要点
  \end{itemize}
  \alert{收尾的关键句或抛给听众的问题}
\end{frame}
```
**注意**：嵌套别超过 3 层；列表项写短语而非整段。

### `description_terms` 术语定义
**何时用**：并列定义若干命名概念（"漂移项 / 扩散项"、"生成建模 / 传输建模"）。常配一张侧图。
**文字容量**：**5~7 条** `\item[术语]`，每条释义 1~2 行；配侧图则降到 ~4 条。
```latex
\begin{frame}{标题}
  \begin{description}
    \item[术语甲] 释义。
    \item[术语乙] 释义。
  \end{description}
\end{frame}
```

---

## B. 文 + 图版式

### `text_fig_split` 左文右图（**最高频**）
**何时用**：图辅助理解、文字讲"为什么/怎么做"，图给直觉或例子。左右可对调（左图右文）。
**默认比例**：`6:4`（文:图）；也常用 `55:45`、`5:5`。
**文字容量**：文字栏（0.6 宽）约 **8~10 行** wrapped，或 **4~6 条** bullet。
```latex
\begin{frame}{标题}
  \begin{columns}
    \column{0.6\textwidth}
      \begin{itemize}\item ...\end{itemize}   % 或推导散文+公式
      > 旁白可放这里
    \column{0.4\textwidth}
      \begin{figure}\centering
        \includegraphics[width=\textwidth]{imgs/xxx.png}
        \caption{...}                          % 可省
      \end{figure}
  \end{columns}
\end{frame}
```
**注意**：右图 `width=\textwidth` 会自动缩到列宽。两栏顶部对齐用 `\begin{columns}[T]`。

### `fig_top_text_bottom` 上图下文
**何时用**："先给一张图，再在下面解释/列点"。
**文字容量**：图占上部 ~55~65% 高，**下方文字最多 3~4 行**（或 3~4 条短 bullet）。
```latex
\begin{frame}{标题}
  \begin{figure}\centering
    \includegraphics[width=0.7\textwidth]{imgs/xxx.png}
  \end{figure}
  \begin{enumerate}\item ...\end{enumerate}    % 或 block / 散文
  收尾散文
\end{frame}
```

### `big_figure` 整页大图
**何时用**：图本身是主角——流程图、算法框图、实验大图。
**默认比例**：图宽 `0.6~1.0\textwidth`，占 ~70~85% 高。
**文字容量**：正文 **0~2 行**。文字较多时，**由排版 agent 决定把它并进标题/副标题栏，
并可取消 `\caption` 与底部文字**，让图最大化。
```latex
\begin{frame}{标题（可把本页唯一一句话写在这或副标题）}
  \begin{figure}\centering
    \includegraphics[width=0.8\textwidth]{imgs/xxx.png}
    \caption{论文/算法名}                       % 排版 agent 可删
  \end{figure}
  % 最多一句话点题（可配 \only<2-> 逐步讲解）；文字多则上移到标题栏
\end{frame}
```

---

## C. 并列 / 对比版式

### `parallel_blocks` 并列概念块
**何时用**："A vs B"、定理+反例、两三个并列设定。
**默认比例**：`5:5`（双栏）或单栏纵向堆叠。
**文字容量**：双栏每块 **~5~6 行**；2×2 则每格 **~3~4 行**。
```latex
\begin{frame}{标题}
  \begin{columns}[T,onlytextwidth]
    \column{0.5\textwidth}
      \begin{block}{概念 A}
        $$ ... $$
      \end{block}
    \column{0.5\textwidth}
      \begin{block}{概念 B}
        \begin{itemize}\item ...\end{itemize}
      \end{block}
  \end{columns}
\end{frame}
```
块类型：`block`（中性）/ `alertblock`（警示、反直觉结论）/ `exampleblock`（例子）。块不嵌套块。

### `image_grid` 图像网格 / 定性对比
**何时用**：结果图、before/after、方法定性对比。
**默认比例**：2-up 各 `0.5w`，或 N×M 各 `0.33w`。
**文字容量**：仅 caption + 至多 **1~2 行**框定文字。
```latex
% 需要 \usepackage{subcaption}
\begin{frame}{标题}
  \begin{figure}\centering
    \begin{subfigure}{0.32\textwidth}\includegraphics[width=\textwidth]{a}\caption{}\end{subfigure}
    \begin{subfigure}{0.32\textwidth}\includegraphics[width=\textwidth]{b}\caption{}\end{subfigure}
    \begin{subfigure}{0.32\textwidth}\includegraphics[width=\textwidth]{c}\caption{}\end{subfigure}
  \end{figure}
\end{frame}
```

### `table_centric` 表格页
**何时用**：定量指标、消融。
**文字容量**：表 **~6~8 行**数据 + 框定文字 1~2 行。
```latex
\begin{frame}{标题}
  \begin{table}\centering
    \begin{tabular}{lcc}
      \toprule 列 & 列 & 列 \\ \midrule
      ... \\
      \bottomrule
    \end{tabular}
    \caption{...}
  \end{table}
\end{frame}
```
**注意**：用 `booktabs`（`\toprule/\midrule/\bottomrule`）；数字对齐用 `siunitx` 的 `S` 列；
也可 `text_fig_split` 式公式左/表右。

---

## D. 特殊版式

### `tikz_concept` 概念关系图
**何时用**：框架/关系/流程图，没有现成图、画图比找图更合适。
**找图阶段会直接用 `source: tikz` 把它画出来**（见 figures 流程文档）。
**文字容量**：图为主时正文 **1~2 行**；若「文左图右」，文字栏同 `text_fig_split`。
```latex
\begin{frame}{标题}
  \begin{figure}\centering
    \resizebox{0.8\textwidth}{!}{
      \begin{tikzpicture}[node distance=2cm,>=Latex]
        \node[draw,rounded corners] (a) {...};
        \node[draw,rounded corners,right=of a] (b) {...};
        \draw[<->] (a) -- (b) node[midway,fill=white]{关系};
      \end{tikzpicture}
    }
  \end{figure}
\end{frame}
```
**注意**：TikZ 图既可**内联**在帧里（方便排版 agent 微调），也可由找图 agent 编译成独立
PDF 再 `\includegraphics`。默认内联，节点文字多时改独立 PDF。

### `paper_info` 论文信息
**何时用**：介绍正在讲的论文。标题/作者/出处/链接，常配 teaser 图或「核心贡献」block。
**文字容量**：贡献 block **~3~5 条** enumerate + 元信息 2~3 行。
```latex
\begin{frame}{论文信息}
  \begin{columns}
    \column{0.6\textwidth}
      \textbf{标题}\\ 作者，出处\\
      \href{https://arxiv.org/abs/xxxx}{arXiv:xxxx}
      \begin{block}{核心贡献}\begin{enumerate}\item ...\end{enumerate}\end{block}
    \column{0.4\textwidth}
      \includegraphics[width=\textwidth]{imgs/teaser.png}
  \end{columns}
\end{frame}
```

### `references` 参考文献
**文字容量**：不限——`[allowframebreaks]` 会自动分页。
```latex
\begin{frame}[allowframebreaks]{参考阅读}
  \begin{thebibliography}{10}
    \beamertemplatearticlebibitems
    \bibitem{key} 作者. \newblock 标题. \newblock \href{url}{出处}, 年.
  \end{thebibliography}
\end{frame}
```
（也可用 `\nocite{*}` + `\bibliography{demo}` + `\bibliographystyle{apalike}`。）

### `code_listing` 代码页（少见）
**文字容量**：代码 **~12~15 行**（`\small`），随字号变化。
```latex
\begin{frame}[fragile]{标题}        % 必须加 [fragile]
  \begin{lstlisting}[language=Python,basicstyle=\small]
  ...
  \end{lstlisting}
\end{frame}
```

---

## 叠加维度（不是版式，每帧可叠加）

- **subtitle 副标题**：`\begin{frame}{标题}{副标题}` 的第二个参数。承载本页**角度/洞见**而非小标签
  （"一种推导方式"、"All flows are one flow"、"关于这个结论的感性理解"）。可空。
  也是 `big_figure` 文字过多时的去处。
- **note 旁白/标注**：按处选，不做全局开关——
  - 口播过渡旁白 → `\texttt{...}`（自成一行）。outline 里写 `> ...` 引用块。
  - 行内高亮关键句/反问 → `\alert{...}`。outline 里写 `==...==`。
  - 粗体关键词 → `\textbf{...}`。outline 里写 `**...**`。
- **reveal 分步**：需要逐步显示时——`\pause`、`\item<2->`、`\only<2->{...}`、
  `\begin{itemize}[<+->]`。outline 里 `reveal: true` 标记该帧需分步，具体节奏交给排版 agent。

## 选版式速查

1. 图是主角？→ `big_figure` / `image_grid` / `tikz_concept`
2. 图是配角？→ `text_fig_split`（讲解为主）/ `fig_top_text_bottom`（先图后讲）
3. 纯推导？→ `derivation_flow`
4. 并列对比概念？→ `parallel_blocks`；并列定义术语？→ `description_terms`
5. 罗列要点/贡献/小结？→ `bullet_points`
6. 数据表？→ `table_centric`
7. 介绍论文本身？→ `paper_info`；结尾文献？→ `references`
