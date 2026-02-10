"""
Calculate rating using 2 rating values.

Arguments:
r1_old : float rating of first player. defaults to 1200
r2_old : float rating of second player. defaults to 1200
winner : winner of match.

"""

# TODO: Internal formulae

from typing import Literal


class Rating:

    def __init__(
        self,
        r1: float = 1200,
        r2: float = 1200,
        w: Literal[-1, 0, 1, 2] = 0,
        print_output: Literal[0, 1] = 0,
    ) -> None:
        old_ratings = (r1, r2)
        self.r1_old = r1
        self.r2_old = r2
        self.winner = w

        self.r_diff = (
            self.r1_old - self.r2_old
            if self.r1_old > self.r2_old
            else self.r2_old - self.r1_old
        )

        # Magic numbers - control multiplier and scaling calculations
        self._eff_x = 75
        self._eff_b = 24

        # Internal calculation results
        self.r_mean = self._calculate_mean()
        self.r_scaling = self._calculate_scaling()
        self.r_polarity = self._define_polarity()
        self.r_balance = self._calculate_balance()
        self.r_multiplier = self._calculate_multiplier()
        self.r_change = self._calculate_change()

        # New ratings
        new_ratings = self.apply_changes()
        self.r1_new = new_ratings[0]
        self.r2_new = new_ratings[1]

        if print_output == 1:
            print(
                f"----------\nSTART OUTPUT\nr_old: {old_ratings}\nr_new: {new_ratings}\nr_change: {self.r_change}\nr_mean: {self.r_mean}\nr_scaling: {self.r_scaling}\nr_polarity: {self.r_polarity}\nr_balance: {self.r_balance}\nEND OUTPUT\n----------"
            )

    def _calculate_mean(self) -> float:
        return round(((self.r1_old + self.r2_old) / 2), 2)

    def _calculate_ratio_to_mean(self) -> tuple[float, float]:
        try:
            return (self.r1_old / self.r_mean, self.r2_old / self.r_mean)
        except ZeroDivisionError:
            return (0, 0)  # defaults failsafe on division by zero

    def _calculate_ratio_to_opp(self) -> tuple[float, float]:
        try:
            return (self.r1_old / self.r2_old, self.r2_old / self.r1_old)
        except ZeroDivisionError:
            return (0, 0)  # failsafe on division by zero

    def _calculate_scaling(self):
        final_ratios = []
        ratio_mean = self._calculate_ratio_to_mean()
        ratio_opp = self._calculate_ratio_to_opp()
        for x in [0, 1]:
            final_ratios.append(round((ratio_mean[x] / ratio_opp[x]), 2))
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
                polarity_r2 = -0.5 if self.r1_old < self.r2_old else 0.5

            case -1:
                pass

        return (polarity_r1, polarity_r2)

    def _calculate_balance(self) -> float:

        return (
            round((self.r_diff / self._eff_b), 2)
            if self.r_diff / self._eff_b >= 20
            else 20
        )

    def _calculate_change(self) -> tuple[float, float]:
        rating_changes = []
        for x in [0, 1]:
            rating_changes.append(
                round(
                    self.r_multiplier
                    * int((self.r_polarity[x] * self.r_scaling[x] * self.r_balance)),
                    2,
                )
            )

        return tuple(rating_changes)

    def _calculate_multiplier(self) -> float:
        return (
            1
            if self.r_diff / self._eff_x <= 1
            else round((self.r_diff / (self._eff_x * 1.675)), 2)
        )

    def apply_changes(self) -> tuple[float, float]:
        return (
            int(self.r1_old + self.r_change[0]),
            int(self.r2_old + self.r_change[1]),
        )
