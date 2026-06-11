# Villa Beamer Theme

A modern and elegant LaTeX Beamer presentation theme designed for academic presentations, originally created for Peking University's Visual-Information Intelligent Learning Lab (Villa).

## Features

- 🎨 Clean and professional design with customizable colors
- 📐 Support for 16:9 aspect ratio presentations
- 🏢 Built-in support for institutional branding (PKU Villa and UESTC variants)
- 📝 Numbered captions and structured frame titles
- 🎯 Section-based navigation with optional section display
- 📊 Well-designed slide layouts for academic content

## Installation

### Option 1: Manual Installation

1. Download or clone this repository
2. Copy the theme files to your LaTeX project directory:
   - `beamerthemevilla.sty`
   - `beamerouterthemevilla.sty`
   - `beamerthemeuestc.sty` (optional, for UESTC variant)
   - `imgs/` folder (for logos)

### Option 2: Local texmf Installation

1. Find your local texmf directory (usually `~/texmf` on Unix or `%USERPROFILE%\texmf` on Windows)
2. Copy the theme files to: `texmf/tex/latex/beamerthemevilla/`
3. Run `texhash` to update the TeX database

## Usage

### Basic Usage

```latex
\documentclass[aspectratio=169]{ctexbeamer}

\mode<presentation>
{
  \usetheme{villa}
}

\title{Your Presentation Title}
\subtitle{Optional Subtitle}
\author{Your Name}
\date{\today}

\begin{document}

\begin{frame}
  \titlepage
\end{frame}

\begin{frame}{Outline}
  \tableofcontents
\end{frame}

% Your content here

\end{document}
```

### Theme Variants

#### UESTC Variant
For University of Electronic Science and Technology of China branding:

```latex
\usetheme{uestc}
```

This automatically applies UESTC colors and logos.

### Theme Options

#### Hide Section Navigation
To hide section information in frame titles:

```latex
\usetheme[nosection]{villa}
```

#### Plain PKU Logo (no lab branding)
To use the plain Peking University logo without the Villa lab wordmark (on both the
title slide and the footer):

```latex
\usetheme[pku]{villa}
```

Options can be combined, e.g. `\usetheme[pku,nosection]{villa}`.

### Customization

#### Colors
The theme defines two main colors that can be customized:

```latex
\definecolor{villatheme}{RGB}{165,48,15}  % Main theme color
\definecolor{villaaccent}{RGB}{225,0,0}   % Accent color
```

#### Logos
Replace the logo files in the `imgs/` directory:
- `pkuvilla.pdf` - Main logo for title slide
- `pkuvilladimmed.pdf` - Dimmed logo for footer
- `pku.pdf` - Plain PKU logo (no lab), for title slide with the `pku` option
- `pkudimmed.pdf` - Plain PKU dimmed logo, for footer with the `pku` option
- `uestc.pdf` - UESTC main logo
- `uestcdimmed.pdf` - UESTC dimmed logo

## Examples

The repository includes several example presentations:

- `slide.tex` - Basic example
- `slide-short.tex` - Short presentation example  
- `slide-full.tex` - Comprehensive example with advanced features

To compile the examples:

```bash
latexmk -pdf slide-full.tex
```

## Requirements

- LaTeX distribution (TeX Live, MiKTeX, etc.)
- Required packages:
  - `tcolorbox`
  - `adjustbox`
  - `ctex` (for Chinese support)
  - Standard Beamer packages

## Project Structure

```
beamerthemevilla/
├── beamerthemevilla.sty          # Main theme file
├── beamerouterthemevilla.sty     # Outer theme (headers/footers)
├── beamerthemeuestc.sty          # UESTC variant
├── imgs/                         # Logo files
│   ├── pkuvilla.pdf
│   ├── pkuvilladimmed.pdf
│   ├── uestc.pdf
│   └── uestcdimmed.pdf
├── slide.tex                     # Basic example
├── slide-short.tex               # Short example
├── slide-full.tex                # Full-featured example
├── demo.bib                      # Bibliography for examples
└── LICENSE                       # MIT License
```
