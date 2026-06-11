# 叙事主线 (narrative)

> 本场报告：向组内同事介绍 `make-slides` 这套 villa Beamer 工作流 skill。
> 这份 deck 本身就是用该 skill 做出来的（dogfooding）。

---

## 一句话主旨

**人定主线、AI 精排**：把论文 / 笔记 / 讨论变成一套手工精排级别的 villa Beamer——
你只需定好"这场报告想讲什么"，逐页苦排的活交给 AI。

---

## 重组逻辑（≠ 软件功能清单）

不按"这个 skill 有哪些命令/脚本"罗列功能，而按**"为什么这套分工能产出手工级质量"**来讲，
好让同事信服、愿意上手。线索：

1. **抛痛点**（1 页）：手工精排 beamer 又慢又累 → 一句话定位 + 一张成品 teaser。
2. **讲透三条理念**（3 页，全场重心）：
   - 混合式分工——按"要不要和人讨论"切阶段；
   - 两个契约文件——`narrative.md` + `outline.yaml` 锁住主线；
   - 亲眼验收——compile→render→看 的循环换来手工级。
3. **一页串起操作**（1 页）：4+1 阶段流水线一图流（把"怎么用"压成一页）。
4. **实物证明**（2 页）：截 Diffusion-RL 成品里最好看的页面作 showcase。
5. **dogfood 收尾**（1 页）：这份 deck 自己就是产物 + 同事怎么开坑。

对比"功能清单式"介绍，这条线先立"为什么值得信"，再给"怎么上手"。

## 关键洞见 / 与"全自动"的分歧

- **质量来自人机分工，而非全自动**：最难、最需要人的 Stage 1（定主线）留给人，
  确定性的精排扇给 AI 并发干。（→ frames: hybrid, pipeline）
- **契约文件是防 AI 跑偏的关键**：`narrative.md`/`outline.yaml` 把主线钉死，
  防止 agent 退回"照搬论文目录"的流水账。（→ frames: contract）
- **"亲眼验收"是达到手工级的关键**：agent 有视觉，让它 compile→render→Read 自看、迭代到不溢出。（→ frames: review）
- **dogfood**：这份 deck 本身由该流程产出，是最有力的证据。（→ frames: itself）

## 刻意弱化 / 不讲

- 不逐一讲每个工具脚本的参数（`buildframe.sh`/`gen-image.sh` 等）——点到为止、给指针。
- 不展开 villa 主题实现、不展开 GPT-Image API、不展开公式（本场 `math_density=0`）。
- 找图的 6 种来源不逐一铺开，只在 showcase 里"让产出说话"（tikz / plot / gpt-image / 截图）。

## 听众与基调

- **听众**：组内同事，已用 Claude Code、懂 beamer 与组会报告。
- **预期已知前提**：知道 beamer/Claude Code 是什么，不必解释；痛点一点就通。
- **公式档位**：`math_density = 0`（概念为主，几乎无 display 公式）。
- **基调**：理念说服 + 实物展示，轻松、自信、少而精；≤10 页短报告（short 模版）。
