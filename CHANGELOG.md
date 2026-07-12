# Changelog — PYculator

## [1.1] — 2025-07-12

### 🔒 Security
- **Replaced `eval()` with `SafeMathParser`** — custom recursive descent parser eliminates arbitrary code execution risk
- **Replaced bare `except`** with specific exception types (`ZeroDivisionError`, `ParseError`, `ValueError`, `TypeError`)
- **Division by zero** now shows "Division by zero" instead of generic "Error"

### ✨ New Features
- **Calculation history** — stores up to 50 entries with expression/result pairs
- **History side panel** — slides in from the left with `QPropertyAnimation` (0 ↔ 260px, 250ms, `OutCubic`)
- **Parentheses buttons `(` `)`** — enables grouped expressions
- **Custom scrollbar** for history list — 14px wide, white handle with border, hidden arrow buttons
- **Keyboard support** — digits, operators, Enter, Backspace, Escape with visual button feedback

### 🎨 UI/UX Redesign
- **Frameless window** with custom title bar and drag support (`mousePressEvent`/`mouseMoveEvent`)
- **Unified body** (`QFrame`) with `#D6D6DA` background and beveled edges:
  - `border-top: 1px solid #FFFFFF` (highlight)
  - `border-left: 1px solid #FFFFFF` (highlight)
  - `border-right: 2px solid #BCBCC0` (shadow)
  - `border-bottom: 5px solid #919196` (deep shadow)
  - `border-radius: 16px`
- **Adaptive window size** — 410×580 (collapsed) / 670×580 (with history panel)
- **Right-aligned layout** (`AlignRight`) — calculator stays fixed, history expands left
- **History panel** uses `background: transparent` to blend with the body
- **Calculator widget** uses `background: transparent` — inherits body color

### 🧮 Calculator Grid
- `QGridLayout` with `setHorizontalSpacing(8)` and `setVerticalSpacing(8)`
- Standard buttons: 74×52px
- "0" button: 156×52px (spans 2 columns)
- `AnimatedButton` — custom `QPushButton` with drop shadow and press/release stylesheet animation
- 4 button styles: `orange_btn` (operators), `gray_btn` (functions), `red_btn` (clear), default (digits)

### 🖥 Display
- `QLineEdit` 324×70px with white background, 12px border-radius, drop shadow
- Auto-scaling font: 36pt / 24pt / 18pt based on expression length

### 🐛 Fixed
- **Percent calculation** — now correctly evaluates `A + B%` as `A + (A × B / 100)` and `A × B%` as `A × (B / 100)`
- **History panel text clipping** — increased panel width to 260px, adjusted margins to `(10, 5, 10, 5)`
- **Button grid stretching** — wrapped in fixed-width container with explicit horizontal/vertical spacing
- **Window resizing on panel toggle** — eliminated by using fixed window size with right-aligned layout