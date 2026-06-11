# 阶段 1.5：公式校对

`outline.yaml` 里公式在阶段 1 就写成最终 LaTeX；这一步专门把它们**编译过一遍 + 查记号一致性**，
保证报告"像手工 beamer 那样严谨"。一个 agent 即可，**只出报告 + 安全修复**，别大改用户内容。

## 怎么做

1. **抽取**：从 `outline.yaml`（并对照 `narrative.md`）抽出每一处行内 `$...$` 和行间 `$$...$$`，记下各自属于哪个 frame `id`。
2. **逐个编译**：在 scratch 目录建 `article` + `\usepackage{amsmath,amssymb,mathtools,bm}`，每个表达式放进自己的 `\[ ... \]` 并前缀 `\texttt{<frame-id>}`，`xelatex -interaction=nonstopmode` 编译。
   - 含中文的表达式（如 `\text{续写}`）在纯 `article` 会报 Missing character——那是字体覆盖问题不是数学错，改用 `ctexart` 复测即可（成品本就是 ctexbeamer，渲染正常）。
   - 有报错就二分/逐条注释定位到具体表达式，给出**确切的最小修复**。
3. **记号一致性**（最有价值的部分）：
   - 同一符号是否全程同义？列一张符号表逐项核（如 `u`=目标速度、`v_\theta`=模型、`v^*`=Bayes 最优、`c`=条件、`R`=reward、`A`=advantage、`\beta`=tilt 温度、`s`=CFG scale）。**一符多义 / 多符一义都要标**。
   - 同一个量在不同帧别用不同记号（如 base 分布别一会 `p_\theta` 一会 `p_{\mathrm{base}}`——`p_\theta` 要留给可训练 policy）。
   - 多字母算子要 `\mathrm{}`/`\text{}` 包（`\mathrm{cond}` 而非 `cond`，否则渲染成斜体相乘）。
   - `<!--label:eq:xxx-->` 标签唯一。
4. **报告**（写到文件 + 返回）：分 `## MUST-FIX`（编译失败/数学错/自相矛盾）、`## NOTATION`（一致性，给推荐统一写法 + 要改哪些帧）、`## OPTIONAL`（不挡编译的小瑕疵）、`## VERDICT`（一句话：N must-fix / M notation / K optional，整体是否 sound）。

## 应用修复（保守）
- **只**改：编译失败的、数学错的、明确的记号统一。每个改动单独 commit、写清原因。
- 风格偏好留 OPTIONAL，别动用户的表达。

> 实战：math_density≤2 的报告通常很干净（0 must-fix）。典型可做的就一两处记号统一，
> 比如把 tilt 律的 base 分布统一成 `p_{\mathrm{base}}`，把 `p_\theta` 留给 rollout policy。
