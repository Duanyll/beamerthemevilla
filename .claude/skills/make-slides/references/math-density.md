# 公式密度 `math_density`（0–3）：带实例的标尺

`math_density` 是 **deck 级**的整体基调——它描述这场报告"推导走多深、公式占多重"，由听众决定
（见各档末尾的「适用听众」）。它不是给每一帧单独打分，而是**全场的重心与上限**：

- deck 设为某档，则**多数帧落在该档及以下**，偶尔有一帧高一档可以，但不应普遍超档。
- 同一份内容，density 越低 → 越多用文字/图/结论替代推导；density 越高 → 越多展开推导链。

下面每档给一句定义 + 一个**可直接照搬的代表帧**（LaTeX 现成），从概念到完整推导横跨各档。

---

## 0 — 概念为主（几乎不出现 display 公式）

只讲概念、动机、结论、背景；至多行内一两个符号。靠文字、列表、图、术语定义承载。

```latex
\begin{frame}{提出 Flow Matching 模型的论文}
    2022 年 10 月有三篇文章从不同理论提出了一类相似的生成模型：
    \begin{description}
        \item[FAIR]      Flow Matching for Generative Modeling
        \item[UT Austin] Rectified Flow
        \item[NYU]       Stochastic Interpolants
    \end{description}
    我们先看 Flow Matching 的理论框架，再介绍 Rectified Flow 的解释。
\end{frame}
```

其它典型 0 档帧：论文背景/动机页、`Insights` 小结、定性结果图页、纯 `bullet_points` 贡献页。
**适用听众**：科普、跨领域 overview、只想知道"是什么/有什么用"的场合。

---

## 1 — 关键式（一个核心公式 + 大量文字解释）

亮出**一个**定义性/核心公式，其余用文字把它讲清楚（常配 `description` 拆解各项）。**陈述**而非推导。

```latex
\begin{frame}{Langevin 动力学}
    Langevin 动力学是 SDE，描述随机过程 $Z_\tau$ 的演化
    \begin{equation*}
        \d Z_{\tau} = \sigma^2\nabla\log\rho(Z_{\tau})\,\d\tau + \sqrt{2}\sigma\,\d W_\tau
    \end{equation*}
    \begin{description}
        \item[漂移项] 系统受力指向概率密度 $\rho$ 增加的方向
        \item[扩散项] 正态噪声，帮助系统脱离局部极值
    \end{description}
    其解是满足 Fokker–Planck 方程的平稳分布。
\end{frame}
```

**适用听众**：课程汇报、跨方向组会；要点出关键数学对象，但不展开。

---

## 2 — 多式（数个公式并列，各自解释，但不逐步推导）

一页里**几个公式并排呈现**（如对比两种 loss、列出几种设定），每个都有一两句说明，
但公式之间是**并列/对照**关系，不是"代入上式得到下式"的链条。

```latex
\begin{frame}{损失函数}
    实际应用的 DDIM 损失函数
    \begin{equation*}
        \mathcal{L}_{\text{DDIM}} = \mathbb{E}\!\left[w(\lambda_t)\tfrac{\d\lambda}{\d t}\|\hat\epsilon-\epsilon\|^2\right],
        \quad \lambda_t=\ln\tfrac{\alpha_t^2}{\sigma_t^2}
    \end{equation*}
    其中 $\lambda_t$ 是对数信噪比，$w(\lambda_t)$ 是人为选定的时间步权重。
    SD3 的 CFM 损失函数
    \begin{equation*}
        \mathcal{L}_{\text{SD3}} = \mathbb{E}\!\left[w(\lambda_t)\|\hat u-u\|^2\right]
    \end{equation*}
    两者实际上都用了手工设计的时间步权重项。
\end{frame}
```

其它典型 2 档帧：「各种插值的 SDE」（三个 `block` 各一个公式）、公式左 + 表格右的对照页。
**适用听众**：方向相近的组会；要看到关键公式的形态与差异，但不必跟完每步推导。

---

## 3 — 完整推导链（一步步代入、化简）

把推导**逐步写出**："定义…→ 写出…→ 代入…→ 得到…"，多个公式由散文串成链条，
常**跨连续多帧**接力推导。最硬核，也最容易把听众讲睡着——
**慎用、且务必匹配听众**。

```latex
\begin{frame}{DDPM 的贝叶斯推导}{一种推导 DDPM 的方式}
    定义前向过程
    \begin{equation*}
        x_t=\alpha_t x_{t-1}+\beta_t\epsilon_t,\quad
        x_t=\bar\alpha_t x_0+\bar\beta_t\bar\epsilon_t
    \end{equation*}
    为反向去噪求 $p(x_{t-1}\mid x_t)$，引入 $x_0$ 作条件写贝叶斯公式
    \begin{equation*}
        p(x_{t-1}\mid x_t,x_0)=\frac{p(x_t\mid x_{t-1})\,p(x_{t-1}\mid x_0)}{p(x_t\mid x_0)}
    \end{equation*}
    代入前向过程、按正态分布运算，得到含未知 $x_0$ 的分布
    \begin{equation*}
        p(x_{t-1}\mid x_t,x_0)\sim\mathcal N\!\left(
            x_{t-1};\ \tfrac{\alpha_t\bar\beta_{t-1}^2}{\bar\beta_t^2}x_t
            +\tfrac{\bar\alpha_{t-1}\beta_t^2}{\bar\beta_t^2}x_0,\
            \tfrac{\bar\beta_{t-1}^2\beta_t^2}{\bar\beta_t^2}I\right)
    \end{equation*}
    % 下一帧接力：训练网络消去 x_0 → 得到迭代公式
\end{frame}
```

版式上多为 `derivation_flow`（单帧 ≤3~4 个 display 公式，超了就拆到下一帧）。
**适用听众**：同方向专家、想吃透推导的组会。

---

## 速记

| 档 | 一句话 | 一帧里 display 公式数 | 公式间关系 |
|---|---|---|---|
| 0 | 概念为主 | 0 | — |
| 1 | 一个关键式 | 1 | 陈述 |
| 2 | 几个公式并列 | 2~3 | 并列/对照 |
| 3 | 完整推导链 | 3~4（可跨帧接力）| 代入→化简 |

选档先问听众，再问"这个点不展开推导，听众能不能接受只给结论"——能，就降档。
