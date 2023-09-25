from dataclasses import dataclass
from typing import Callable


@dataclass
class lr2_params:
    c_a: Callable[[], str]  # Concentration in atmosphere / outside (mg / m^3)
    c_h: Callable[[], str]  # Concentration inside (mg / m^3)
    t_out: Callable[[], str]  # Time outside (hours)
    t_in: Callable[[], str]  # Time inside (hours)
    v_out: Callable[[], str]  # inhalation rate outside (m^3 / hour)
    v_in: Callable[[], str]  # inhalation rate inside (m^3 / hour)
    e_f: Callable[[], str]  # influence frequency (days / year)
    e_d: Callable[[], str]  # influence duration (years)
    b_w: Callable[[], str]  # body weight (kg)
    a_t: Callable[[], str]  # exposure averaging period (years)

    @property
    def average_daily_substance_doze(self):
        variables = [self.c_a, self.t_out, self.v_out, self.c_h, self.t_in, self.v_in, self.e_f, self.e_d, self.b_w, self.a_t]
        for var in variables:
            self.__setattr__(var.__name__, int(var()))

        return (
               (self.c_a *
                 self.t_out *
                 self.v_out +
                 self.c_h *
                 self.t_in *
                 self.v_in)
                * self.e_f
                * self.e_d
        ) / (self.b_w * self.a_t * 365)


@dataclass
class lr3_params:
    mass: float  # mass of a substance that is released into the atmosphere above the norm (tons)
    minimum_wage: float  # amount of the minimum wage on the date of detection of the offense
    relative_danger_coef: float  # a dimensionless indicator of the relative danger of a substance
    territory_coef: float  # coefficient that takes into account territorial socio-economic features
    pollution_coef: float  # coefficient that depends on the level of atmospheric pollution by a given substance

    @property
    def get_material_damages(self):
        return (
                self.mass
                * 1.1
                * self.minimum_wage
                * self.relative_danger_coef
                * self.territory_coef
                * self.pollution_coef
        )
