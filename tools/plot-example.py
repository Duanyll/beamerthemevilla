#!/usr/bin/env python3
"""Self-contained example of the make-slides *plot* best-practice.

It synthesises a reward-curve-like dataset (no external CSV needed) and renders
it the way the skill recommends, so you can run it as-is and then copy/adapt it
for a real deck. The points it demonstrates:

  * the plotting CODE is saved (this file) — figures stay reproducible;
  * each figure is exported as BOTH .pdf (vector — what beamer embeds) and
    .png (raster — what the agent eyeballs);
  * seaborn's built-in theme gives a clean, consistent look, tied to the villa
    brick-red so plots match the deck;
  * val is sparse (recorded every ~20 steps) → dropna() before plotting it;
  * matplotlib has no CJK font by default → labels stay English, Chinese goes in
    the beamer caption/body.

Run:
  uv run --with numpy --with pandas --with matplotlib --with seaborn \
      python tools/plot-example.py

For a real deck, point OUT at imgs/ and read your own CSV instead of synth_run().
"""
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

REPO = pathlib.Path(__file__).resolve().parent.parent
OUT = REPO / ".build" / "plot-example"          # throwaway preview dir (gitignored)
OUT.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="talk")
BRICK = "#A5300F"   # villatheme — val (the metric that matters)
STEEL = "#3B6EA5"   # rollout
plt.rcParams.update({"axes.titlesize": 15, "axes.labelsize": 13,
                     "legend.fontsize": 12, "figure.dpi": 110})


def synth_run(seed, n=200, val_every=20):
    """Fake a training run: a noisy rising rollout curve + a sparse val curve.

    Mirrors the typical CSV schema:
        step, rollout_reward_mean, rollout_reward_std, val_reward_mean, val_reward_std
    """
    rng = np.random.default_rng(seed)
    step = np.arange(n)
    curve = 0.85 - 0.55 * np.exp(-step / 60.0)          # saturating learning curve
    rollout_mean = curve + rng.normal(0, 0.015, n)
    rollout_std = 0.04 + 0.02 * np.exp(-step / 80.0)
    val_mean = np.full(n, np.nan)                         # sparse: most rows empty
    idx = step % val_every == 0
    val_mean[idx] = curve[idx] + 0.03 + rng.normal(0, 0.01, idx.sum())
    return pd.DataFrame({"step": step,
                         "rollout_reward_mean": rollout_mean,
                         "rollout_reward_std": rollout_std,
                         "val_reward_mean": val_mean})


def _save(fig, stem):
    fig.tight_layout()
    fig.savefig(OUT / f"{stem}.pdf")              # vector → beamer
    fig.savefig(OUT / f"{stem}.png", dpi=150)     # raster → agent inspection
    plt.close(fig)
    print("wrote", OUT / f"{stem}.pdf", "+ .png")


def plot_run(df, stem, title, figsize=(6.0, 4.0)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df.step, df.rollout_reward_mean, color=STEEL, lw=1.6, label="rollout")
    ax.fill_between(df.step,
                    df.rollout_reward_mean - df.rollout_reward_std,
                    df.rollout_reward_mean + df.rollout_reward_std,
                    color=STEEL, alpha=0.15)
    v = df.dropna(subset=["val_reward_mean"])     # val is sparse → drop empties
    ax.plot(v.step, v.val_reward_mean, color=BRICK, lw=2.4, marker="o", ms=5, label="val")
    ax.set_xlabel("step"); ax.set_ylabel("reward"); ax.set_title(title)
    ax.legend(loc="lower right", frameon=True)
    _save(fig, stem)


if __name__ == "__main__":
    plot_run(synth_run(seed=0), "example-curve", "example reward curve")
    print("done — preview under", OUT)
