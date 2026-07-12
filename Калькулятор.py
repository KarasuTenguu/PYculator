__version__ = "1.1"


import sys
import math
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem,
                             QGraphicsDropShadowEffect, QFrame)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QByteArray
from PySide6.QtGui import QFont, QColor, QKeyEvent


# ============================================================
# Безопасный парсер математических выражений (вместо eval)
# ============================================================
class SafeMathParser:
    class ParseError(Exception):
        pass
    
    def __init__(self, expression: str):
        self.expression = expression.replace(' ', '')
        self.pos = 0
        self.current_char = self.expression[0] if self.expression else ''
    
    def _advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.expression):
            self.current_char = self.expression[self.pos]
        else:
            self.current_char = ''
    
    def _parse_number(self) -> float:
        result = ''
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self._advance()
        if not result:
            raise self.ParseError(f"Ожидалось число на позиции {self.pos}")
        if result.count('.') > 1:
            raise self.ParseError("Некорректное число (больше одной точки)")
        return float(result)
    
    def _parse_factor(self) -> float:
        if self.current_char == '-':
            self._advance()
            return -self._parse_factor()
        if self.current_char == '+':
            self._advance()
            return self._parse_factor()
        if self.current_char == '√':
            self._advance()
            val = self._parse_factor()
            if val < 0:
                raise self.ParseError("Корень из отрицательного числа")
            return math.sqrt(val)
        if self.current_char == '(':
            self._advance()
            result = self._parse_expression()
            if self.current_char != ')':
                raise self.ParseError(f"Ожидалась ')' на позиции {self.pos}")
            self._advance()
            return result
        return self._parse_number()
    
    def _parse_term(self) -> float:
        result = self._parse_factor()
        while self.current_char in ('*', '/'):
            op = self.current_char
            self._advance()
            right = self._parse_factor()
            if op == '*':
                result *= right
            elif op == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= right
        return result
    
    def _parse_expression(self) -> float:
        result = self._parse_term()
        while self.current_char in ('+', '-'):
            op = self.current_char
            self._advance()
            right = self._parse_term()
            if op == '+':
                result += right
            elif op == '-':
                result -= right
        return result
    
    def evaluate(self) -> float:
        if not self.expression:
            raise self.ParseError("Пустое выражение")
        result = self._parse_expression()
        if self.current_char:
            raise self.ParseError(f"Неожиданный символ '{self.current_char}' на позиции {self.pos}")
        return result


class AnimatedButton(QPushButton):
    def __init__(self, text, style_type='', parent=None):
        super().__init__(text, parent)
        self.style_type = style_type
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(8)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(3)
        self.shadow.setColor(QColor(0, 0, 0, 40)) 
        self.setGraphicsEffect(self.shadow)
        
        self.set_normal_style()

    def set_normal_style(self):
        if self.style_type == 'orange_btn':
            self.setStyleSheet("background-color: #e5a93b; color: white; font-weight: bold; border: none; border-radius: 14px; font-size: 20px; padding: 0px;")
        elif self.style_type == 'gray_btn':
            self.setStyleSheet("background-color: #e5e5ea; color: #1c1c1e; border: none; border-radius: 14px; font-size: 20px; padding: 0px;")
        elif self.style_type == 'red_btn':
            self.setStyleSheet("background-color: #ff3b30; color: white; font-weight: bold; border: none; border-radius: 14px; font-size: 20px; padding: 0px;")
        elif self.style_type == 'close_btn':
            self.setStyleSheet("background-color: #e5e5ea; color: #1c1c1e; font-weight: bold; border: none; border-radius: 14px; font-size: 20px; padding: 0px;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #1c1c1e; border: none; border-radius: 14px; font-size: 20px; padding: 0px;")

    def press_animation(self):
        if self.style_type == 'orange_btn':
            self.setStyleSheet("background-color: #cc7f08; color: white; font-weight: bold; border: none; border-radius: 14px; font-size: 20px; padding-top: 4px;")
        elif self.style_type == 'gray_btn':
            self.setStyleSheet("background-color: #d1d1d6; color: #1c1c1e; border: none; border-radius: 14px; font-size: 20px; padding-top: 4px;")
        elif self.style_type == 'red_btn':
            self.setStyleSheet("background-color: #cc2a20; color: white; font-weight: bold; border: none; border-radius: 14px; font-size: 20px; padding-top: 4px;")
        elif self.style_type == 'close_btn':
            self.setStyleSheet("background-color: #d1d1d6; color: #1c1c1e; border: none; border-radius: 14px; font-size: 20px; padding-top: 4px;")
        else:
            self.setStyleSheet("background-color: #f2f2f7; color: #1c1c1e; border: none; border-radius: 14px; font-size: 20px; padding-top: 4px;")
        self.shadow.setYOffset(1)
        self.shadow.setBlurRadius(3)

    def release_animation(self):
        self.set_normal_style()
        self.shadow.setYOffset(3)
        self.shadow.setBlurRadius(8)

    def mousePressEvent(self, event):
        self.press_animation()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.release_animation()
        super().mouseReleaseEvent(event)


# ============================================================
# Боковая панель истории
# ============================================================
class HistorySidePanel(QFrame):
    """Боковая панель истории. Показывается/скрывается через show()/hide().
    Окно меняет размер: 360x530 (скрыта) или 620x530 (открыта)."""

    PANEL_WIDTH = 260

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")
        self.setFixedWidth(self.PANEL_WIDTH)
        self.hide()  # Изначально скрыта

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 0, 10, 5)
        layout.setSpacing(8)

        # Шапка истории (40px, как title bar калькулятора)
        history_header = QWidget()
        history_header.setStyleSheet("background: transparent;")
        history_header.setFixedHeight(40)
        header_layout = QHBoxLayout(history_header)
        header_layout.setContentsMargins(4, 0, 0, 0)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        title = QPushButton("📋  История")
        title.setStyleSheet(
            "background-color: transparent; color: #1c1c1e; font-size: 16px; "
            "font-weight: bold; border: none; text-align: left; padding: 4px;"
        )
        title.setEnabled(False)
        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addWidget(history_header)

        # Список истории
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(
            "QListWidget {"
            "  background-color: #ffffff; color: #1c1c1e; border: none; border-radius: 10px;"
            "  font-size: 13px; padding: 4px; margin-top: 12px; outline: none;"
            "}"
            "QListWidget::item {"
            "  color: #1c1c1e;"
            "}"
            "QScrollBar:vertical {"
            "  background: #f0f0f2;"
            "  width: 14px;"
            "  margin: 0px;"
            "  border-radius: 4px;"
            "}"
            "QScrollBar::handle:vertical {"
            "  background: #ffffff;"
            "  border: 1px solid #d1d1d6;"
            "  border-bottom: 2px solid #b5b5ba;"
            "  border-radius: 6px;"
            "  min-height: 30px;"
            "}"
            "QScrollBar::handle:vertical:hover {"
            "  background: #f2f2f7;"
            "}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {"
            "  background: none;"
            "  height: 0px;"
            "}"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {"
            "  background: none;"
            "}"
        )
        self.list_widget.setSpacing(2)
        self.list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.list_widget)

        # Кнопка очистки истории — только иконка корзины
        self.clear_btn = QPushButton("🗑")
        self.clear_btn.setFixedSize(55, 45)
        self.clear_btn.setStyleSheet(
            "background-color: #f2f2f7; color: #1c1c1e; font-size: 20px; font-weight: bold; "
            "border: 1px solid #d1d1d6; border-bottom: 2px solid #b5b5ba; "
            "border-radius: 10px; padding: 0px;"
        )
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # Выравнивание по центру через контейнер
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addStretch()
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def update_history(self, history: list) -> None:
        self.list_widget.clear()
        for entry in history:
            item = QListWidgetItem(entry)
            item.setData(Qt.ItemDataRole.UserRole, entry.split(" = ")[0] if " = " in entry else entry)
            self.list_widget.addItem(item)
        self.list_widget.scrollToBottom()

    def clear_history(self) -> None:
        self.list_widget.clear()


class Calculator(QWidget):
    MAX_EXPRESSION_LENGTH = 20
    MAX_HISTORY_ITEMS = 50

    def __init__(self):
        super().__init__()
        self.expression = ""
        self.is_result_shown = False
        self.history = []
        self._drag_pos = None  # Для перетаскивания окна
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PYculator")
        # Убираем стандартную рамку Windows, сплошной фон
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        # Начальный размер — только калькулятор (360 + отступы 25+25 = 410)
        self.setFixedSize(410, 580)
        self.setStyleSheet("font-family: 'Segoe UI', Arial, sans-serif;")

        # --- Единый корпус (main_body) с глубокими фасками ---
        self.main_body = QFrame(self)
        self.main_body.setStyleSheet(
            "QFrame {"
            "  background-color: #d6d6da;"
            "  border-radius: 16px;"
            "  border-top: 1px solid #ffffff;"
            "  border-left: 1px solid #ffffff;"
            "  border-right: 2px solid #bcbcc0;"
            "  border-bottom: 5px solid #919196;"
            "}"
        )

        # Layout корпуса
        body_layout = QHBoxLayout(self.main_body)
        body_layout.setContentsMargins(25, 25, 25, 25)
        body_layout.setSpacing(0)
        body_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # --- Панель истории (прозрачная, слева) ---
        self.side_panel = HistorySidePanel(self)
        self.side_panel.list_widget.itemClicked.connect(self._on_history_item_clicked)
        self.side_panel.clear_btn.clicked.connect(self._clear_history)
        body_layout.addWidget(self.side_panel)

        # --- Калькулятор (прозрачный, справа) ---
        self.calc_widget = QWidget()
        self.calc_widget.setStyleSheet("background: transparent; border: none;")
        self.calc_widget.setFixedSize(360, 530)
        body_layout.addWidget(self.calc_widget)
        calc_layout = QVBoxLayout(self.calc_widget)
        calc_layout.setContentsMargins(18, 0, 18, 18)
        calc_layout.setSpacing(12)

        # --- Title Bar (только над калькулятором) ---
        title_bar = QWidget()
        title_bar.setStyleSheet("background: transparent;")
        title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(4, 0, 4, 0)

        # Название "PYculator" по центру
        calc_title = QPushButton("PYculator")
        calc_title.setStyleSheet(
            "background-color: transparent; color: #1c1c1e; font-size: 16px; "
            "font-weight: bold; border: none; text-align: center; padding: 4px;"
        )
        calc_title.setEnabled(False)
        title_layout.addWidget(calc_title)

        title_layout.addStretch()

        # Кнопка Свернуть
        self.min_btn = QPushButton("—")
        self.min_btn.setFixedSize(40, 30)
        self.min_btn.setStyleSheet(
            "background-color: #e5e5ea; color: #1c1c1e; font-weight: bold; border: none; "
            "border-radius: 8px; font-size: 16px;"
        )
        self.min_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.min_btn.clicked.connect(self.showMinimized)
        title_layout.addWidget(self.min_btn)

        # Кнопка Закрыть
        self.close_win_btn = QPushButton("✕")
        self.close_win_btn.setFixedSize(40, 30)
        self.close_win_btn.setStyleSheet(
            "background-color: #ff3b30; color: white; font-weight: bold; border: none; "
            "border-radius: 8px; font-size: 16px;"
        )
        self.close_win_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_win_btn.clicked.connect(self.close)
        title_layout.addWidget(self.close_win_btn)

        calc_layout.addWidget(title_bar)

        # Дисплей
        self.display = QLineEdit()
        self.display.setFixedSize(324, 70)
        self.display.setStyleSheet("background-color: #ffffff; color: #1c1c1e; border: none; border-radius: 12px; padding: 15px;")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.update_display_font()

        display_shadow = QGraphicsDropShadowEffect(self)
        display_shadow.setBlurRadius(15)
        display_shadow.setXOffset(0)
        display_shadow.setYOffset(4)
        display_shadow.setColor(QColor(0, 0, 0, 30))
        self.display.setGraphicsEffect(display_shadow)

        calc_layout.addWidget(self.display)

        # Сетка кнопок
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setHorizontalSpacing(8)
        grid_layout.setVerticalSpacing(8)

        buttons = [
            ('C', 0, 0, 'gray_btn'), ('√', 0, 1, 'gray_btn'), ('%', 0, 2, 'gray_btn'), ('←', 0, 3, 'gray_btn'),
            ('7', 1, 0, ''),         ('8', 1, 1, ''),         ('9', 1, 2, ''),         ('/', 1, 3, 'orange_btn'),
            ('4', 2, 0, ''),         ('5', 2, 1, ''),         ('6', 2, 2, ''),         ('*', 2, 3, 'orange_btn'),
            ('1', 3, 0, ''),         ('2', 3, 1, ''),         ('3', 3, 2, ''),         ('-', 3, 3, 'orange_btn'),
            ('0', 4, 0, ''),         ('.', 4, 2, ''),         ('+', 4, 3, 'orange_btn'),
            ('📋', 5, 0, 'gray_btn'), ('(', 5, 1, 'gray_btn'), (')', 5, 2, 'gray_btn'), ('=', 5, 3, 'orange_btn'),
        ]

        self.button_objects = {}

        for text, row, col, style_class in buttons:
            btn = AnimatedButton(text, style_class)

            if text == '0':
                btn.setFixedSize(156, 52)
                grid_layout.addWidget(btn, row, col, 1, 2)
            else:
                btn.setFixedSize(74, 52)
                grid_layout.addWidget(btn, row, col)

            btn.clicked.connect(lambda ch=None, t=text: self.on_button_click(t))
            self.button_objects[text] = btn

        calc_layout.addLayout(grid_layout)

        # Главный layout окна — только main_body
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_body)
        self.setLayout(main_layout)

    # --- Перетаскивание окна (frameless) ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos is not None:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = None
            event.accept()

    def _toggle_side_panel(self) -> None:
        """Открыть/закрыть боковую панель истории."""
        self.side_panel.update_history(self.history)

        if self.side_panel.isVisible():
            # Закрываем: сначала hide, потом сжимаем окно
            self.side_panel.hide()
            self.setFixedSize(410, 580)
        else:
            # Открываем: сначала show, потом расширяем окно
            self.side_panel.show()
            self.setFixedSize(670, 580)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.text()       
        key_sym = event.key()    

        if key in '0123456789+-*/.%()':
            self.trigger_keyboard_animation(key)
            self.on_button_click(str(key))
        elif key.lower() == 'x' or key == ',':
            mapped_key = '*' if key.lower() == 'x' else '.'
            self.trigger_keyboard_animation(mapped_key)
            self.on_button_click(str(mapped_key))
        elif key_sym in [Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Equal]:
            self.trigger_keyboard_animation('=')
            self.on_button_click('=')
        elif key_sym == Qt.Key.Key_Backspace:
            self.trigger_keyboard_animation('←')
            self.on_button_click('←')
        elif key_sym == Qt.Key.Key_Escape:
            self.trigger_keyboard_animation('C')
            self.on_button_click('C')

    def trigger_keyboard_animation(self, target_text):
        if target_text in self.button_objects:
            btn = self.button_objects[target_text]
            btn.press_animation()
            QTimer.singleShot(100, btn.release_animation)

    def update_display_font(self):
        text_length = len(self.display.text())
        font = QFont('Segoe UI')
        font.setBold(True)

        if text_length > 14:
            font.setPointSize(18)
        elif text_length > 9:
            font.setPointSize(24)
        else:
            font.setPointSize(36)

        self.display.setFont(font)

    def _on_history_item_clicked(self, item: QListWidgetItem) -> None:
        expression = item.data(Qt.ItemDataRole.UserRole)
        if expression:
            self.expression = expression
            self.is_result_shown = False
            self.display.setText(self.expression)
            self.update_display_font()

    def _clear_history(self) -> None:
        self.history.clear()
        self.side_panel.clear_history()

    def _add_to_history(self, expression: str, result: str) -> None:
        entry = f"{expression} = {result}"
        self.history.append(entry)
        if len(self.history) > self.MAX_HISTORY_ITEMS:
            self.history.pop(0)
        if self.side_panel.isVisible():
            self.side_panel.update_history(self.history)

    def _safe_evaluate(self, expr: str) -> str:
        try:
            parser = SafeMathParser(expr)
            result = parser.evaluate()
            if isinstance(result, float):
                if result == float('inf') or result == float('-inf'):
                    return "Error"
                if math.isnan(result):
                    return "Error"
                result = round(result, 10)
                if result == int(result):
                    result = int(result)
            return str(result)
        except ZeroDivisionError:
            return "Division by zero"
        except (SafeMathParser.ParseError, ValueError, TypeError):
            return "Error"

    def _handle_percent(self) -> None:
        try:
            operators = ['+', '-', '*', '/']
            found_op = None
            for op in operators:
                if op in self.expression:
                    found_op = op
                    break
            if found_op:
                parts = self.expression.split(found_op)
                if len(parts) == 2 and parts[0] and parts[1]:
                    left = parts[0]
                    right = parts[1]
                    base = float(SafeMathParser(left).evaluate())
                    percent = float(right)
                    if found_op in ['*', '/']:
                        calc_value = percent / 100
                        self.expression = f"{left}{found_op}{calc_value}"
                    else:
                        calc_value = base * (percent / 100)
                        self.expression = f"{left}{found_op}{calc_value}"
            else:
                self.expression = str(float(self.expression) / 100)
            self.is_result_shown = False
        except (SafeMathParser.ParseError, ValueError, ZeroDivisionError, TypeError):
            self.expression = "Error"
            self.is_result_shown = True

    def on_button_click(self, text):
        if text == 'C':
            self.expression = ""
            self.is_result_shown = False
        elif text == '←': 
            if self.expression and self.expression not in ("Error", "Division by zero"):
                self.expression = self.expression[:-1]
                self.is_result_shown = False
        elif text == '📋':
            self._toggle_side_panel()
        elif text == '=':
            if self.expression:
                result = self._safe_evaluate(self.expression)
                self._add_to_history(self.expression, result)
                self.expression = result
                self.is_result_shown = True
        elif text == '√':
            if self.expression:
                current_val = self._safe_evaluate(self.expression)
                if current_val in ("Error", "Division by zero"):
                    self.expression = current_val
                else:
                    result = self._safe_evaluate(f"√({current_val})")
                    self._add_to_history(f"√({self.expression})", result)
                    self.expression = result
            else:
                self.expression = "Error"
            self.is_result_shown = True
        elif text == '%':
            self._handle_percent()
        else:
            if self.is_result_shown:
                if text in '0123456789.()':
                    self.expression = ""
                self.is_result_shown = False 
            if self.expression in ("Error", "Division by zero"):
                self.expression = ""
            if len(self.expression) < self.MAX_EXPRESSION_LENGTH:
                self.expression += text

        self.display.setText(self.expression)
        self.update_display_font()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())
