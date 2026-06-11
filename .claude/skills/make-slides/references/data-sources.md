# 数据 / 素材源 (data sources)

deck 级 `resources` 字段声明"这场报告能用的素材在哪"，让阶段 2 找图 agent 不必现场摸索。
找图时按 `figures[].source` 取用对应资源。

## `outline.yaml` 里的 `resources`

```yaml
resources:
  papers:                                  # paper_crop 来源
    - id: fm
      path: refs/flow-matching.pdf
      note: "FM 原论文（ICLR'23）；Fig.3 棋盘格、Fig.4 路径设计"
  trackio: "http://192.168.5.133:7860/"    # plot 来源：实验指标 dashboard
  others:                                  # 主页 / 视频 / 数据集 等
    - "项目主页 https://..."
```

`figures[].from` 可引用这里的 `id`/路径，找图 agent 据此定位。

---

## 各类源 → 找图 agent 怎么用

### 论文 PDF（`source: paper_crop`）
- 路径在 `resources.papers[].path`。用 `pdftoppm` / `pdfcrop --bbox` / `pdftocairo` 定位页码并裁剪目标子图。
- 截完**亲眼看**：论文图缩到 slide 上常常字太小 → 裁掉无关白边、只留核心子图，必要时按区域裁。

### trackio 实验指标（`source: plot`）
本场实例见 `resources.trackio`。trackio 是 HF 的轻量实验跟踪（与 wandb API 兼容），**数据开放可取**。
**首选：拉指标数据 → 自己用 matplotlib/seaborn 重画**（矢量、与 beamer 风格统一），而不是截 dashboard 图。

取工具用 `uv`（本机约定，勿全局装）：
```bash
# 列项目 / 运行 / 指标（--json 便于程序读取）
uv run --with trackio trackio list projects --json
uv run --with trackio trackio get metric --project <P> --run <R> --metric <loss> --json
# 复杂查询用只读 SQL
uv run --with trackio trackio query project --project <P> --sql "SELECT step, loss FROM metrics WHERE ..."
```
或用 Gradio 客户端直接连实例：
```python
# uv run --with gradio_client python - <<'PY'
from gradio_client import Client
c = Client("http://192.168.5.133:7860/")
print(c.predict(api_name="/get_all_projects"))
print(c.predict("<project>", api_name="/get_runs_for_project"))
print(c.predict("<project>", "<run>", "<metric>", api_name="/get_metric_values"))
# PY
```
> trackio 仍在 beta：**端点/参数名以实例 dashboard 页脚的「Use via API or MCP」为准**，
> 或查 https://huggingface.co/docs/trackio/api_mcp_server 。
> 拿到序列后画成 PDF；**实在拉不到数据再退而截 dashboard 图**（位图、清晰度差，最后手段）。

### 其它来源
- `web` / `gpt_image` / `tikz` / `provided`：见 `outline-schema.md` 的 source 表与 `gpt-image.md`。
- **自备图**（`provided`，如自己跑的实验结果截图）：放好后在 `figures[].path` 直接指向，不必登记进 `resources`。
