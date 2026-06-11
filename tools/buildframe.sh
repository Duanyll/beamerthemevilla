#!/usr/bin/env bash
# Build & render ONE frame in an isolated dir, for the typesetting loop.
#
#   bash tools/buildframe.sh <frame-id> [section-name]
#
# Reads frames/<frame-id>.tex, wraps it with the shared preamble + villa theme
# (full template, so the section header renders realistically), compiles with
# XeLaTeX, and rasterises every page to PNG at 150dpi.
#
# Output on success:  PASS <id> pages=N  +  the PNG paths under .build/frames/<id>/
# Output on failure:  FAIL <id>  +  last 40 log lines  (exit 1)
#
# Fully isolated: each id gets its own .build/frames/<id>/; repo resources
# (preamble.tex, frames/, imgs/, *.sty) are found via TEXINPUTS, never copied,
# so many agents can run this concurrently without conflict.
set -euo pipefail
ID="${1:?usage: buildframe.sh <frame-id> [section]}"
SEC="${2:-占位章节}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
BD="$REPO/.build/frames/$ID"
rm -rf "$BD"; mkdir -p "$BD"

cat > "$BD/harness.tex" <<EOF
\\documentclass[aspectratio=169]{ctexbeamer}
\\input{preamble.tex}
\\usetheme{villa}
% Placeholder title/author — this harness only renders one frame to eyeball its
% layout, so the chrome text is irrelevant. The real deck's title comes from outline.yaml.
\\title[示例报告]{示例报告}
\\author[段宇乐]{段宇乐}
\\date{\\today}
\\begin{document}
\\section{$SEC}
\\input{frames/$ID.tex}
\\end{document}
EOF

cd "$BD"
export TEXINPUTS="$REPO:"
if xelatex -interaction=nonstopmode -halt-on-error harness.tex > xelatex.log 2>&1; then
  pdftoppm -png -r 150 harness.pdf page >/dev/null 2>&1 || true
  n=$(ls page*.png 2>/dev/null | wc -l | tr -d ' ')
  echo "PASS $ID pages=$n"
  for p in "$BD"/page*.png; do [ -f "$p" ] && echo "  $p"; done
  # Overfull/underfull hints help the agent spot silent overflow.
  grep -E 'Overfull|Underfull' xelatex.log | head -5 || true
else
  echo "FAIL $ID"
  echo "--- $BD/xelatex.log (last 40) ---"
  tail -40 xelatex.log
  exit 1
fi
