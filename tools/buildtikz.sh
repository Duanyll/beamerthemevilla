#!/usr/bin/env bash
# Preview ONE TikZ figure on a real slide, for the figure-creation loop.
#
#   bash tools/buildtikz.sh <path/to/foo.tikz.tex>
#
# Wraps the snippet in a ctexbeamer frame using the SAME preamble the deck uses
# (so tikz libraries / fonts / colours match), compiles, renders to PNG.
# Use this to eyeball legibility + the figure's must_show checklist before the
# typeset stage drops it into its real frame.
set -euo pipefail
TIKZ="${1:?usage: buildtikz.sh <path/to/foo.tikz.tex>}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
NAME="$(basename "$TIKZ" .tikz.tex)"
BD="$REPO/.build/tikz/$NAME"
rm -rf "$BD"; mkdir -p "$BD"

cat > "$BD/harness.tex" <<EOF
\\documentclass[aspectratio=169]{ctexbeamer}
\\input{preamble.tex}
\\usetheme{villa}
\\begin{document}
\\begin{frame}{TikZ 预览：$NAME}
\\begin{figure}\\centering
\\input{$TIKZ}
\\end{figure}
\\end{frame}
\\end{document}
EOF

cd "$BD"
export TEXINPUTS="$REPO:"
if xelatex -interaction=nonstopmode -halt-on-error harness.tex > xelatex.log 2>&1; then
  pdftoppm -png -r 150 harness.pdf page >/dev/null 2>&1 || true
  echo "PASS tikz $NAME -> $BD/page-1.png"
  grep -E 'Overfull|Underfull' xelatex.log | head -5 || true
else
  echo "FAIL tikz $NAME"
  echo "--- $BD/xelatex.log (last 40) ---"
  tail -40 xelatex.log
  exit 1
fi
