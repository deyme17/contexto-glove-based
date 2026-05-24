from __future__ import annotations

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

from core.hints import Hint
from utils.palette import HINT_BG, HINT_BORDER, HINT_TEXT


class HintBanner(QLabel):
    """Widget for displaying hints to the user."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setStyleSheet(f"""
            QLabel {{
                background: {HINT_BG};
                color: {HINT_TEXT};
                border: 1px solid {HINT_BORDER};
                border-radius: 8px;
                padding: 10px 16px;
                font-size: 13px;
            }}
        """)
        self.hide()

    def show_hint(self, hint: Hint) -> None:
        """Displays a hint in the banner."""
        if hint.kind == "direction":
            self.setText(f'Think about:  <b>"{hint.word}"</b>')
        else:
            self.setText(f'Your word relates to <b>"{hint.tip1}"</b> + <b>"{hint.tip2}"</b>')
        self.show()