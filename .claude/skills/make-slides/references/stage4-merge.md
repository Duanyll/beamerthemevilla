# 阶段 4：合并终检

把所有页拼成完整文档，全量编译，逐页复核风格统一 / 内容连贯 / 格式正确。主对话主导 + 人复核。

## 步骤

1. **拼装**：`uv run --with pyyaml python tools/gen-slides.py` —— 读 `outline.yaml` 生成 `slides.tex`：
   - documentclass + `\input{preamble.tex}` + `\usetheme{villa}`（短报告 `[nosection]`）；
   - 标题（含 `——` 自动拆成 title/subtitle）、作者、日期；
   - full 模版加 `\AtBeginSection` 目录页；
   - titlepage + 全局目录 + 按 `outline.yaml` 顺序 `\section`/`\subsection`/`\input{frames/<id>.tex}`。
   - **slides.tex 是自动生成的，别手改**；要改改 `outline.yaml` 或对应 `frames/<id>.tex` 再重跑。
2. **全量编译**（跑两遍，处理目录/引用）：`latexmk -xelatex -interaction=nonstopmode -halt-on-error slides.tex`。
   - **别跑 `latexmk -C`**（会删掉仓库里 tracked 的 PDF）。
   - 看 `Overfull/Underfull` 数量；sub-pixel（<1pt）可忽略。
3. **逐页自看**（关键，编排者亲自做——你有视觉）：
   - `pdftoppm -png -r 100 slides.pdf .build/deck/p` 渲染全部页；用 PIL（`uv run --with pillow`）拼成 contact sheet，`Read` 通览；可疑页再 `-r 170 -f N -l N` 放大单看。
   - 查：溢出/裁切、标题撑破圈、图过大过小、公式越界、残留 markdown（`==`/`**`/`{{fig}}`）、跨页风格不一致、缺图。
   - **可选**：派一个 final-review agent 读全部页、返回"哪几页要修"清单（adversarial 终检），比只信各页 agent 的自述更稳。
4. **修问题**：定位到具体 `frames/<id>.tex` 改 → `buildframe.sh` 单页复看 → 改好后重跑 `gen-slides.py` + `latexmk` → 复核那几页。
   > ⚠️ **换图 / 改图尺寸 / 换格式（PNG↔PDF、改 aspect）后，务必对用到该图的每一页重跑 `buildframe.sh` 复看**——
   > 图的有效尺寸一变，版面就可能溢出或失衡（矢量 PDF 的有效尺寸常和原 PNG 不同）。别只重编全本就当完事。
5. **交付**：`slides.pdf` + 简短说明（做了哪些适配/取舍、需要用户复核的地方，如自动改短的 section 名、被截断的实验等）。git commit 备份。

## 终检清单
- [ ] 全量编译 0 error，Overfull 仅 sub-pixel。
- [ ] 标题页 / 目录 / 各 section 目录 / 页码 / 页脚（短标题·日期·作者·页码）正常。
- [ ] 每页不溢出、图文比例舒适、字号风格跨页一致。
- [ ] 公式记号与阶段 1.5 校对一致；引用页（allowframebreaks）正常。
- [ ] 叙事连贯：和 `narrative.md` 的弧线一致，没有退回论文流水。

> **验收基准（什么叫"过关"）**：一份几十页的长报告，全量编译 0 error；残留 Overfull 只剩
> sub-pixel（<1pt）或个别居中后**肉眼不可见**的 cosmetic hbox；tikz/plot/paper_crop/gpt-image
> 多类图混排风格统一；逐页过了排版自看 + 一轮 adversarial 终检。达到这条线就算手工精排水准。
