from .meters import SimilarityMeter, CosineMeter, EuclideanMeter, ManhattanMeter, ChessboardMeter
from .game import GameState, new_game
from .hints import HintEngine, Hint

METERS: list[SimilarityMeter] = [
    CosineMeter(),
    EuclideanMeter(),
    ManhattanMeter(),
    ChessboardMeter(),
]