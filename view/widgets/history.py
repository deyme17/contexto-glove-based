from __future__ import annotations

from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel,
    QScrollArea, QWidget, QVBoxLayout
)
from PyQt6.QtCore import Qt

from core.game import Guess
from utils.palette import (
    SURFACE, TEXT, BG, MUTED, rank_color
)

####################################################################
####################### Guess history widget #######################
####################################################################

class GuessRow(QFrame):
    """Widget representing a single guess in the guess history."""
    def __init__(self, guess: Guess, parent=None) -> None:
        super().__init__(parent)
        color = rank_color(guess.rank)
        self.setFixedHeight(44)
        self.setStyleSheet(f"""
            GuessRow {{
                background: {SURFACE};
                border: 1px solid {color}44;
                border-radius: 8px;
            }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 14, 0)
        layout.setSpacing(0)

        # rank badge
        badge = QLabel(f"#{guess.rank}")
        badge.setFixedWidth(56)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"""
            background: {color};
            color: #0F1117;
            font-weight: 700;
            font-size: 13px;
            border-radius: 7px 0 0 7px;
        """)
        layout.addWidget(badge)

        # word
        word_lbl = QLabel(guess.word)
        word_lbl.setStyleSheet(f"color: {TEXT}; font-size: 14px; padding-left: 12px;")
        layout.addWidget(word_lbl, stretch=1)

        # score
        score_lbl = QLabel(f"{guess.score:.1f}%")
        score_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        score_lbl.setStyleSheet(f"color: {color}; font-weight: 700; font-size: 13px;")
        layout.addWidget(score_lbl)



####################################################################
### Widget to display the history of guesses in the current game ###
####################################################################

class GuessHistory(QScrollArea):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setStyleSheet(f"background: {BG}; border: none;")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._inner = QWidget()
        self._layout = QVBoxLayout(self._inner)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setSpacing(4)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._empty = QLabel("Type a word above to start guessing")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setStyleSheet(f"color: {MUTED}; font-size: 14px; padding: 40px;")
        self._layout.addWidget(self._empty)

        self.setWidget(self._inner)

    def refresh(self, guesses: list[Guess]) -> None:
        # clear
        while self._layout.count():
            item = self._layout.takeAt(0)
            widget = item.widget()
            if widget:
                if widget == self._empty:
                    continue
                widget.deleteLater()

        if not guesses:
            self._empty.show()
            self._layout.addWidget(self._empty)
            return
        self._empty.hide()
        for g in guesses:
            self._layout.addWidget(GuessRow(g))

        self.verticalScrollBar().setValue(0)