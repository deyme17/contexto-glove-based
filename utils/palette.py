BG = "#0F1117"
SURFACE = "#1A1D27"
BORDER = "#2A2D3A"
TEXT = "#E8E9F0"
MUTED = "#6B7090"
ACCENT = "#7C6AF7"

RANK_HOT = "#22C55E"
RANK_WARM = "#F59E0B"
RANK_COLD = "#EF4444"

HINT_BG = "#1E2340"
HINT_BORDER = "#3B4280"
HINT_TEXT = "#A5B0FF"


def rank_color(rank: int) -> str:
    if rank <= 10:
        return RANK_HOT
    if rank <= 40:
        return RANK_WARM
    return RANK_COLD