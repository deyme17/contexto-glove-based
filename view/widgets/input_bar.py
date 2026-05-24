from __future__ import annotations
from typing import Callable, List

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QCompleter
)
from PyQt6.QtCore import Qt

from utils.palette import SURFACE, BORDER, TEXT, ACCENT


def _btn(text: str, primary: bool = False) -> QPushButton:
    """Helper to create a styled QPushButton."""
    b = QPushButton(text)
    if primary:
        b.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT}; color: #fff;
                border: none; border-radius: 7px;
                padding: 9px 18px; font-size: 13px;
            }}
            QPushButton:hover {{ background: #6A59E0; }}
            QPushButton:pressed {{ background: #584DC0; }}
        """)
    else:
        b.setStyleSheet(f"""
            QPushButton {{
                background: {SURFACE}; color: {TEXT};
                border: 1px solid {BORDER}; border-radius: 7px;
                padding: 9px 14px; font-size: 13px;
            }}
            QPushButton:hover {{ border-color: {ACCENT}; color: #A5B0FF; }}
            QPushButton:pressed {{ background: #252840; }}
        """)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    return b


class InputBar(QWidget):
    """Widget for entering guesses and requesting hints/new game."""
    def __init__(self,
                 on_guess: Callable[[str], None],
                 on_hint_direction: Callable[[], None],
                 on_hint_composition: Callable[[], None],
                 on_new_game: Callable[[], None],
                 parent=None) -> None:
        """
        Args:
            on_guess: Callback when user submits a guess. Receives the guessed word.
            on_hint_direction: Callback when user requests a direction hint.
            on_hint_composition: Callback when user requests a composition hint.
            on_new_game: Callback when user requests to start a new game.
        """
        super().__init__(parent)
        self._on_guess = on_guess

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # hint + new game buttons
        row1 = QHBoxLayout()
        row1.setSpacing(8)

        h1_btn = _btn("Direction hint")
        h1_btn.clicked.connect(on_hint_direction)

        h2_btn = _btn("Composition hint")
        h2_btn.clicked.connect(on_hint_composition)

        new_btn = _btn("New game")
        new_btn.clicked.connect(on_new_game)

        row1.addWidget(h1_btn)
        row1.addWidget(h2_btn)
        row1.addStretch()
        row1.addWidget(new_btn)

        # input + check button
        row2 = QHBoxLayout()
        row2.setSpacing(8)

        self._entry = QLineEdit()
        self._entry.setPlaceholderText("Type a word...")
        self._entry.setStyleSheet(f"""
            QLineEdit {{
                background: {SURFACE}; color: {TEXT};
                border: 1px solid {BORDER}; border-radius: 7px;
                padding: 9px 14px; font-size: 15px;
            }}
            QLineEdit:focus {{ border-color: {ACCENT}; }}
        """)
        self._entry.returnPressed.connect(self._submit)

        self._check_btn = _btn("Check", primary=True)
        self._check_btn.clicked.connect(self._submit)

        row2.addWidget(self._entry)
        row2.addWidget(self._check_btn)

        layout.addLayout(row1)
        layout.addLayout(row2)

    def set_vocab(self, words: List[str]) -> None:
        """
        Sets the vocabulary for autocomplete suggestions in the input field.
        Args:
            words: List of valid words to use for autocomplete.
        """
        completer = QCompleter(words)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchStartsWith)
        completer.popup().setStyleSheet(f"""
            QListView {{
                background: {SURFACE}; color: {TEXT};
                border: 1px solid {BORDER}; border-radius: 7px;
                font-size: 13px;
            }}
            QListView::item:selected {{ background: {ACCENT}; color: #fff; }}
        """)
        self._entry.setCompleter(completer)

    def _submit(self) -> None:
        """Handles submission of a guess."""
        word = self._entry.text().strip()
        if word:
            self._on_guess(word)
            self._entry.clear()

    def focus(self) -> None:
        """Sets focus to the input field."""
        self._entry.setFocus()