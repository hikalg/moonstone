"""
Docstring for moonstone.moon_performance.moonperformance
"""

from typing import Literal


class Playscore:

    def __init__(self, pp: list[int] = [], np: list[int] = []):
        self.pos_points : list[int] = pp
        self.neg_points : list[int] = np

        self._scaling_pos = []
        self._scaling_neg = []
        self.padding = 0.2531

    def set_scaling(self, mode: Literal[1, -1], scaling: list[float]) -> list[float]:

        match mode:
            case 1:
                if len(scaling) != len(self.pos_points):
                    raise ValueError("You must define scaling for all scores")

                self._scaling_pos = scaling
                return self._scaling_pos
            case -1:
                if len(scaling) != len(self.neg_points):
                    raise ValueError("You must define scaling for all scores")

                self._scaling_neg = scaling
                return self._scaling_neg
            case _:
                return []

    def calculate_playscore(self) -> float:
        playscore_pos = 0
        playscore_neg = 0
        padding = self.padding

        for x in range(len(self.pos_points)):
            playscore_pos = playscore_pos + (self._scaling_pos[x] * self.pos_points[x])

        for x in range(len(self.neg_points)):
            playscore_neg = playscore_neg + (self._scaling_neg[x] * self.neg_points[x])
        
        return round((playscore_pos - playscore_neg + padding), 2)
    

playscore = Playscore([16, 3], [15])
playscore.set_scaling(1, [1.235, 0.234])
playscore.set_scaling(-1, [1.442])
print(playscore.calculate_playscore())
