# 阶段 1：大纲设计（交互）

整条流水线**最难、最需要人**的一步。产出 `narrative.md` + `outline.yaml` 两个契约文件。
**全程在主对话里和用户讨论完成，不要派后台 agent**（它无法和用户来回对话）。

## 已知失败模式（要主动对抗）

1. **退回论文目录**：agent 容易照搬原文的章节流水，而报告需要一条**论点驱动**的弧线。
   → 先写 `narrative.md` 把"重组逻辑（≠ 论文目录）"钉死，后续一切以它为纲。
2. **公式密度失控**：要么堆满推导、要么全靠嘴说。
   → 用 `math_density`（0–3，deck 级**上限**）定调，参考 [`math-density.md`](math-density.md) 的真实分档实例。
3. **页面留虚条目**："讨论 X""介绍一下 Y"——排版阶段无从下手。
   → 每帧 `body` 写**实际文字 + 最终公式**。

## 步骤

### 1. 摸清源材料与场景
读论文/笔记/实验记录。问清楚（用 `AskUserQuestion` 收关键岔路）：听众是谁、什么前提可直接用不必解释、要讲多深、长报告还是短分享、有哪些自备素材（实验图、trackio、PDF）。
若是**论文分享**，结构参考导师的 8 点法 [`report-structure.md`](report-structure.md)——**只借结构、不借风格**。

### 2. 先写 `narrative.md`（和用户对齐主线）
按 [`narrative-template.md`](narrative-template.md) 写：一句话主旨 / 重组逻辑 / 关键洞见与分歧 / 刻意弱化 / 听众与基调。
**这一步要和用户反复讨论**——主线对了，后面才不跑偏。把它当成全场的"宪法"。

### 3. 据 `narrative.md` 写满 `outline.yaml`
schema 见 [`outline-schema.md`](outline-schema.md)。要点：

- **公式在这一步就写成最终 LaTeX**（用户明确要求）。排版阶段只在实在放不下时简化；所以这里写全、写对，交给阶段 1.5 校对。
- 每帧选一个 `layout`（版式名见 [`layouts.md`](layouts.md)），`layout_hint` 用**自然语言**给排版建议（"左文右图约六成""下方最多 3 行"）——**不写死像素**，左右比例/图宽留给阶段 3。
- `figures[]` 写清每张图的 `source`/`intent`/`must_show`，让阶段 2 的 agent 一上手就知道找什么、怎么验收。
- **section 名 ≤8 汉字 / 20 字母，最好 4 字**（full 模版进左上圈；short 模版则是每个帧标题进圈，须很短）。详见 `layouts.md` 模版长度一节。
- `resources` 声明本场素材源（PDF / trackio / 主页），见 [`data-sources.md`](data-sources.md)。

### 4. 和用户过一遍
把 outline 给用户审（尤其 section 划分、每页要点、公式取舍、哪些刻意弱化）。改到用户满意再进阶段 1.5。

## 完成标准
- `narrative.md` 主线清晰，用户认可。
- `outline.yaml` 每帧内容落实、公式完整、版式与图规格齐全，section 名够短，`resources` 写明。
