"""
Calculate rating using 2 rating values.

Arguments:
r1_old : float rating of first player. defaults to 1200
r2_old : float rating of second player. defaults to 1200
winner : winner of match.

"""

# TODO: Internal formulae

from typing import Literal


class Rating():

    def __init__(
        self, r1: float = 1200, r2: float = 1200, w: Literal[-1, 0, 1, 2] = 0
    ) -> None:

        self.r1_old = r1
        self.r2_old = r2
        self.winner = w
        
        self.r_diff = (
            self.r1_old - self.r2_old
            if self.r1_old > self.r2_old
            else self.r2_old - self.r1_old
        )
        
        # Magic numbers - control multiplier and scaling calculations
        self._magic_number_multi = 75
        self._magic_number_scaling = 24

        # Internal calculation results
        self._ratings_mean = self._calculate_mean()
        self._ratio_mean = self._calculate_ratio_to_mean()
        self._ratio_opp = self._calculate_ratio_to_opp()
        self._ratio_final = self._calculate_final_ratio()
        self._polarity = self._define_polarity()
        self._scaling = self._calculate_scaling()
        self._multiplier = self._calculate_multiplier()
        self._rating_changes = self._calculate_rating_change()
        
        # New ratings
        self.new_ratings = self.apply_rating_changes()

        print(
            f"{self._ratings_mean} {self._ratio_final} {self._polarity} {self._scaling} {self._rating_changes} {self.new_ratings}"
        )

    def _calculate_mean(self) -> float:
        return round(((self.r1_old + self.r2_old) / 2), 2)

    def _calculate_ratio_to_mean(self) -> tuple[float, float]:
        try:
            return (self.r1_old / self._ratings_mean, self.r2_old / self._ratings_mean)
        except ZeroDivisionError:
            return (0, 0) # defaults failsafe on division by zero

    def _calculate_ratio_to_opp(self) -> tuple[float, float]:
        try:
            return (self.r1_old / self.r2_old, self.r2_old / self.r1_old)
        except ZeroDivisionError:
            return (0, 0) # failsafe on division by zero

    def _calculate_final_ratio(self):
        final_ratios = []
        for x in [0, 1]:
            final_ratios.append(round((self._ratio_mean[x] / self._ratio_opp[x]), 2))
        return tuple(final_ratios)

    def _define_polarity(self) -> tuple[float, float]:
        polarity_r1 = 0
        polarity_r2 = 0

        match self.winner:
            case 1:
                polarity_r1 = 1
                polarity_r2 = -1
            case 2:
                polarity_r1 = -1
                polarity_r2 = 1
            case 0:
                if self.r1_old == self.r2_old:
                    pass

                polarity_r1 = -0.5 if self.r1_old > self.r2_old else 0.5
                polarity_r1 = -0.5 if self.r1_old < self.r2_old else 0.5

            case -1:
                pass

        return (polarity_r1, polarity_r2)

    def _calculate_scaling(self) -> float:
        
        return round((self.r_diff / self._magic_number_scaling), 2) if self.r_diff / self._magic_number_scaling >= 20 else 20

    def _calculate_rating_change(self) -> tuple[float, float]:
        rating_changes = []
        for x in [0, 1]:
            rating_changes.append(
                round(self._multiplier * int((self._ratio_final[x] * self._polarity[x] * self._scaling)), 2)
            )

        return tuple(rating_changes)
    
    def _calculate_multiplier(self) -> float:
        return 1 if self.r_diff / self._magic_number_multi <= 1 else round((self.r_diff / (self._magic_number_multi * 1.25)), 2)
        
    
    def apply_rating_changes(self) -> tuple[float, float]:
        return (
            self.r1_old + self._rating_changes[0], self.r1_old + self._rating_changes[1]
        )


rating1 = Rating(1500, 1200, 1)
rating1 = Rating(1800, 1200, 2)
