# PYculator 🧮

**PYculator** — современный калькулятор для Windows / A modern desktop calculator for Windows.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PySide6](https://img.shields.io/badge/PySide6-6.8%2B-green)
![Version](https://img.shields.io/badge/version-1.1-orange)

---

## 🇷🇺 Русский

### ✨ Возможности

- **Базовые операции**: `+`, `−`, `×`, `÷`
- **Проценты**: корректный расчёт `A + B%` как `A + (A × B / 100)` и `A × B%` как `A × (B / 100)`
- **Квадратный корень**: `√`
- **Скобки**: `(` `)` для групповых выражений
- **История вычислений**: анимированная боковая панель, до 50 записей
- **Клавиатурный ввод**: цифры, операторы, Enter, Backspace, Escape
- **Анимированные кнопки**: визуальная обратная связь при нажатии
- **Безопасность**: собственный рекурсивный парсер (`SafeMathParser`) вместо `eval()`

### 🚀 Установка и запуск

**Требования:** Python 3.10+, PySide6 6.8+

```bash
pip install PySide6
python "Калькулятор.py"
```

**Сборка в .exe:**
```bash
pip install pyinstaller
pyinstaller "Калькулятор.spec"
```

Готовый `.exe` появится в папке `dist/`.

### 📖 Руководство пользователя

**Основные операции:**
1. Введите число (кнопками или с клавиатуры)
2. Выберите операцию: `+`, `−`, `×`, `÷`
3. Введите второе число
4. Нажмите `=` или `Enter`

**Проценты:**

| Выражение | Расчёт | Пример |
|-----------|--------|--------|
| `A + B%` | `A + (A × B / 100)` | `200 + 10%` = `220` |
| `A − B%` | `A − (A × B / 100)` | `200 − 10%` = `180` |
| `A × B%` | `A × (B / 100)` | `200 × 10%` = `20` |
| `A ÷ B%` | `A ÷ (B / 100)` | `200 ÷ 10%` = `2000` |

**Квадратный корень:** введите число, нажмите `√`. Пример: `9 √` → `3`

**Скобки:** `(2 + 3) × 4` → `20`

**История:** кнопка **📋** (слева вверху) открывает панель истории. Нажмите на запись, чтобы восстановить выражение. **🗑** — очистить историю. Клавиша **`H`** — переключить панель.

**Горячие клавиши:**

| Клавиша | Действие |
|---------|----------|
| `0`–`9` | Ввод цифр |
| `+`, `-`, `*`, `/` | Операторы |
| `.` или `,` | Десятичный разделитель |
| `Enter` | Вычислить результат |
| `Backspace` | Удалить последний символ |
| `Escape` | Очистить всё (`C`) |
| `H` | Открыть/закрыть историю |

**Управление окном:** перетащите заголовок для перемещения. `—` свернуть, `✕` закрыть.

---

## 🇬🇧 English

### ✨ Features

- **Basic operations**: `+`, `−`, `×`, `÷`
- **Percentages**: correctly evaluates `A + B%` as `A + (A × B / 100)` and `A × B%` as `A × (B / 100)`
- **Square root**: `√`
- **Parentheses**: `(` `)` for grouped expressions
- **Calculation history**: animated side panel, stores up to 50 entries
- **Keyboard input**: digits, operators, Enter, Backspace, Escape
- **Animated buttons**: visual feedback on press/release
- **Security**: custom recursive descent parser (`SafeMathParser`) instead of `eval()`

### 🚀 Installation & Setup

**Prerequisites:** Python 3.10+, PySide6 6.8+

```bash
pip install PySide6
python "Калькулятор.py"
```

**Build to .exe:**
```bash
pip install pyinstaller
pyinstaller "Калькулятор.spec"
```

The compiled `.exe` will be in the `dist/` folder.

### 📖 User Guide

**Basic Usage:**
1. Enter a number (click buttons or use keyboard)
2. Select an operation: `+`, `−`, `×`, `÷`
3. Enter the second number
4. Press `=` or `Enter`

**Percentages:**

| Expression | Calculation | Example |
|-----------|-------------|---------|
| `A + B%` | `A + (A × B / 100)` | `200 + 10%` = `220` |
| `A − B%` | `A − (A × B / 100)` | `200 − 10%` = `180` |
| `A × B%` | `A × (B / 100)` | `200 × 10%` = `20` |
| `A ÷ B%` | `A ÷ (B / 100)` | `200 ÷ 10%` = `2000` |

**Square Root:** enter a number, press `√`. Example: `9 √` → `3`

**Parentheses:** `(2 + 3) × 4` → `20`

**History:** Click **📋** (top-left) to open the history panel. Click any entry to restore that expression. **🗑** clears all history. Press **`H`** to toggle the panel.

**Keyboard Shortcuts:**

| Key | Action |
|-----|--------|
| `0`–`9` | Enter digits |
| `+`, `-`, `*`, `/` | Operators |
| `.` or `,` | Decimal separator |
| `Enter` | Calculate result |
| `Backspace` | Delete last character |
| `Escape` | Clear all (`C`) |
| `H` | Toggle history panel |

**Window Controls:** drag the title bar to move. `—` to minimize, `✕` to close.

---

## 🏗 Architecture / Архитектура

```
Калькулятор.py
├── SafeMathParser        # Recursive descent parser (replaces eval)
├── AnimatedButton        # Custom QPushButton with press/release animation
├── HistorySidePanel      # Sliding history panel (QPropertyAnimation)
└── Calculator            # Main application window
    ├── init_ui()         # Builds the interface
    ├── on_button_click() # Handles all button clicks
    ├── _safe_evaluate()  # Safe expression evaluation
    └── _handle_percent() # Percent calculation logic
```

## 📜 Changelog / История версий

See [CHANGELOG.md](CHANGELOG.md)

## 📄 License / Лицензия

MIT