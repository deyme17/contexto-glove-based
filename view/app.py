from __future__ import annotations
from typing import List, Optional

import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QMessageBox, QFrame
)

from core import (
    METERS, SimilarityMeter, GameState, new_game
)
from utils.palette import (
    BG, SURFACE, BORDER, TEXT, MUTED, ACCENT, rank_color
)
from view.widgets.input_bar import InputBar
from view.widgets.hint_banner import HintBanner
from view.widgets.history import GuessHistory



class ContextoApp(QMainWindow):
    """Main Contexto app window. Manages overall game state and UI layout."""
    def __init__(self, words: List[str], matrix: np.ndarray) -> None:
        super().__init__()
        self._words = words
        self._matrix = matrix
        self._state: Optional[GameState] = None

        self.setWindowTitle("Contexto")
        self.setMinimumSize(700, 600)
        self.resize(740, 680)
        self._apply_global_style()
        self._build_ui()
        self._new_game()

    def _apply_global_style(self) -> None:
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ background: {BG}; color: {TEXT}; }}
            QScrollBar:vertical {{
                background: {BG}; width: 6px; border: none;
            }}
            QScrollBar::handle:vertical {{
                background: {BORDER}; border-radius: 3px; min-height: 20px;
            }}
            QComboBox {{
                background: {SURFACE}; color: {TEXT};
                border: 1px solid {BORDER}; border-radius: 6px;
                padding: 4px 10px;
            }}
            QComboBox:hover {{ border-color: {ACCENT}; }}
            QComboBox QAbstractItemView {{
                background: {SURFACE}; color: {TEXT};
                selection-background-color: {ACCENT};
            }}
        """)

    def _build_ui(self) -> None:
        """Builds the main UI layout."""
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)

        # title + metric selector
        header = QHBoxLayout()
        title = QLabel("CONTEXTO")
        title.setStyleSheet(f"color: {ACCENT}; font-size: 22px; font-weight: 700; letter-spacing: 3px;")
        header.addWidget(title)
        header.addStretch()
        header.addWidget(QLabel("Metric:"))
        self._metric_box = QComboBox()
        combo_font = self._metric_box.font()
        combo_font.setPointSize(12)
        self._metric_box.setFont(combo_font)
        self._metric_box.addItems([m.name for m in METERS])
        self._metric_box.currentTextChanged.connect(self._on_metric_change)
        header.addWidget(self._metric_box)
        layout.addLayout(header)

        # status
        self._status = QLabel("0 guesses")
        self._status.setStyleSheet(f"color: {MUTED}; font-size: 12px;")
        layout.addWidget(self._status)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"color: {BORDER};")
        layout.addWidget(line)

        # input
        self._input_bar = InputBar(
            on_guess=self._on_guess,
            on_hint_direction=lambda: self._on_hint("direction"),
            on_hint_composition=lambda: self._on_hint("composition"),
            on_new_game=self._new_game,
        )
        layout.addWidget(self._input_bar)

        # hint
        self._hint_banner = HintBanner()
        layout.addWidget(self._hint_banner)

        # history
        self._history = GuessHistory()
        layout.addWidget(self._history, stretch=1)

    def _new_game(self) -> None:
        """Starts a new game. Resets all relevant state and UI components."""
        meter = self._current_meter()
        self._state = new_game(self._words, self._matrix, meter=meter)
        self._history.refresh([])
        self._hint_banner.hide()
        self._status.setText("0 guesses")
        self._status.setStyleSheet(f"color: {MUTED}; font-size: 12px;")
        self._input_bar.set_vocab(self._words)
        self._input_bar.focus()

    def _current_meter(self) -> SimilarityMeter:
        """Returns the currently selected similarity meter."""
        name = self._metric_box.currentText()
        return next(m for m in METERS if m.name == name)

    def _on_guess(self, word: str) -> None:
        """Handles a guess submission. Updates game state and UI accordingly."""
        if self._state is None or self._state.won:
            return

        if any(g.word.lower() == word.lower() for g in self._state.guesses):
            QMessageBox.information(self, "Duplicate word", 
                                    f'You have already guessed "{word}".')
            return

        guess = self._state.guess(word)
        if guess is None:
            QMessageBox.warning(self, "Unknown word",
                                f'"{word}" is not in the vocabulary.')
            return

        self._history.refresh(self._state.guesses)

        n = self._state.guess_count
        label = "guess" if n == 1 else "guesses"

        if self._state.won:
            self._status.setText(f'Found "{self._state.target}" in {n} {label}!')
            self._status.setStyleSheet(f"color: {rank_color(1)}; font-size: 13px; font-weight: 600;")
        else:
            self._status.setText(f"{n} {label}")

    def _on_hint(self, kind: str) -> None:
        """Handles hint requests. Displays the appropriate hint based on the current game state."""
        if self._state is None:
            return
        self._hint_banner.show_hint(self._state.hint(kind))

    def _on_metric_change(self, _name: str) -> None:
        """Handles changes to the selected similarity metric. Resets the current game state."""
        if self._state is None:
            return
        self._state.change_meter(self._current_meter())
        self._history.refresh(self._state.guesses)