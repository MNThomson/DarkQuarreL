from .battlegroundsDuel import BattlegroundsDuel
from .solo import Solo


def make(str):
    if str == "Battlegrounds-Duel":
        return BattlegroundsDuel()
    if str == "Solo":
        return Solo()
