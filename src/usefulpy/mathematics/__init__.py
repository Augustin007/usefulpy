'''
usefulpy mathematics

Several mathematical functions plopped together.

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   mathematics.py contains many mathematical functions.
  Version 0.0.1:
   An updated description and various bug fixes. Cleaner looking code with more
   comments.
  Version 0.0.2:
   Some small bug fixes
   Raises warnings at unfinished sections
 0.1
  Version 0.1.0
   Separated into sections and placed into a folder of its own
  Version 0.1.1
   Mostly some small bugfixes and clearer commenting throughout
  Version 0.1.2
   Several bugfixes, some work on algebraic solver and improvements on eq
  Version 0.1.3
   Heavy improvements in nmath, small bugfixes throughout
  Version 0.1.4
   Small improvement throughout.
 0.2
  Version 0.2.0
   Heavy bugfixing throughout. Deprecated algebraic solver and eq
  Version 0.2.1
   More bugfixing, some more functions. Efficiency increased
1
 1.0
  Version 1.0.0
   Entirety of folder restructured. Much improved use of mathfuncs. Expression
   check has taken the place of eq and algebraic solver. Basic CAS implemented
   for the new mathfunc-eq-solver merge. Greater efficiency and power to most
   other areas. nmath made much smaller, most of its functionality has been
   moved to the mathfunc file.
'''

# INFO #
__version__ = '1.0.0'
__author__ = 'Augustin Garcia'
if __name__ == '__main__':
    __package__ = 'usefulpy.mathematics'
__all__ = ('comb', 'copysign', 'erf', 'erfc', 'fabs', 'fmod', 'fsum', 'gamma', 'lgamma', 'modf', 'nextafter', 'perm',
           'remainder', 'trunc', 'ulp', 'ldexp', 'frexp', 'fromNumBaseFormat', 'basenum', 'Interval', 'interval',
           'unified_interval', 'is_interval', 'vector', 'matrix', 'quaternion', 'i', 'j', 'k', 'Avogadro', 'Boltzmann',
           'Btu', 'Btu_IT', 'Btu_th', 'G', 'Julian_year', 'N_A', 'Planck', 'R', 'Rydberg', 'Stefan_Boltzmann', 'Wien',
           'acre', 'alpha', 'angstrom', 'arcmin', 'arcminute', 'arcsec', 'arcsecond', 'astronomical_unit', 'atm',
           'atmosphere', 'atomic_mass', 'atto', 'au', 'bar', 'barrel', 'bbl', 'blob', 'c', 'calorie', 'calorie_IT',
           'calorie_th', 'carat', 'centi', 'day', 'deci', 'degree', 'degree_Fahrenheit', 'deka', 'dyn', 'dyne', 'e',
           'eV', 'electron_mass', 'electron_volt', 'elementary_charge', 'epsilon_0', 'erg', 'exa', 'exbi', 'femto',
           'fermi', 'fine_structure', 'fluid_ounce', 'fluid_ounce_US', 'fluid_ounce_imp', 'foot', 'g', 'gallon',
           'gallon_US', 'gallon_imp', 'gas_constant', 'gibi', 'giga', 'golden', 'golden_ratio', 'grain', 'gram',
           'gravitational_constant', 'h', 'hbar', 'hectare', 'hecto', 'horsepower', 'hour', 'hp', 'inch', 'inf', 'infj',
           'kappa', 'kgf', 'kibi', 'kilo', 'kilogram_force', 'kmh', 'knot', 'lb', 'lbf', 'light_year', 'liter', 'litre',
           'long_ton', 'm_e', 'm_n', 'm_p', 'm_u', 'mach', 'mebi', 'mega', 'metric_ton', 'micro', 'micron', 'mil', 'mile',
           'milli', 'minute', 'mmHg', 'monster', 'mph', 'mu_0', 'nan', 'nanj', 'nano', 'nautical_mile', 'neg_inf', 'neg_infj',
           'neutron_mass', 'ounce', 'oz', 'parsec', 'pebi', 'peta', 'phi', 'phi_', 'pi', 'pico', 'point', 'pound', 'pound_force',
           'proton_mass', 'psi', 'pt', 'rho', 'short_ton', 'sigma', 'slinch', 'slug', 'speed_of_light', 'speed_of_sound', 'stone',
           'supergoldenpsi', 'survey_foot', 'survey_mile', 'tau', 'tebi', 'tera', 'ton_TNT', 'torr', 'troy_ounce', 'troy_pound',
           'u', 'week', 'yard', 'year', 'yobi', 'yotta', 'zebi', 'zepto', 'zero_Celsius', 'zetta', 'κ', 'π', 'ρ', 'τ', 'φ', 'φ_',
           'ψ', 'S', 'acos', 'acosh', 'acot', 'acoth', 'acsc', 'acsch', 'asec', 'asech', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
           'binomial_coeficient', 'cas_variable', 'cbrt', 'ceil', 'cis', 'cos', 'cosh', 'cot', 'coth', 'csc', 'csch', 'cube', 'exp',
           'expm1', 'floor', 'from_str', 'icbrt', 'is_constant', 'isqrt', 'ln', 'log', 'log1p', 'log2', 'mathfunc', 'mathfunction',
           'polynomial', 'sec', 'sech', 'sigmoid', 'sin', 'sinh', 'sqrt', 'square', 'tan', 'tanh', 'tesser', 'x', 'y', 'z', 'AngleType',
           'Composite', 'Factor', 'Heron', 'LawofCos', 'LawofSin', 'Prime', 'TriangleType', 'acute', 'circle', 'digit_prod', 'digit_sum',
           'dist', 'equilateral', 'even', 'factorial', 'gcd', 'hypot', 'isTriangle', 'isclose', 'isfinite', 'isinf', 'isnan',
           'isosceles', 'lcm', 'obtuse', 'odd', 'persistance', 'persistance_generator', 'phase', 'polar', 'primes_till', 'prod',
           'product', 'rect', 'right', 'rt', 'scalene', 'segmented_sieve', 'sieve', 'straight', 'summation', 'triangle')

# IMPORTS #
from math import comb, copysign, erf, erfc, fabs, fmod, fsum, gamma, lgamma
from math import modf, nextafter, perm, remainder, trunc, ulp, ldexp, frexp
from .constants import Avogadro, Boltzmann, Btu, Btu_IT, Btu_th, G, Julian_year, N_A, Planck, R, Rydberg
from .constants import Stefan_Boltzmann, Wien, acre, alpha, angstrom, arcmin, arcminute, arcsec, arcsecond
from .constants import astronomical_unit, atm, atmosphere, atomic_mass, atto, au, bar, barrel, bbl, blob, c
from .constants import calorie, calorie_IT, calorie_th, carat, centi, day, deci, degree, degree_Fahrenheit
from .constants import deka, dyn, dyne, e, eV, electron_mass, electron_volt, elementary_charge, epsilon_0
from .constants import erg, exa, exbi, femto, fermi, fine_structure, fluid_ounce, fluid_ounce_US, fluid_ounce_imp
from .constants import foot, g, gallon, gallon_US, gallon_imp, gas_constant, gibi, giga, golden, golden_ratio, grain
from .constants import gram, gravitational_constant, h, hbar, hectare, hecto, horsepower, hour, hp, inch, inf, infj
from .constants import kappa, kgf, kibi, kilo, kilogram_force, kmh, knot, lb, lbf, light_year, liter, litre, long_ton
from .constants import m_e, m_n, m_p, m_u, mach, mebi, mega, metric_ton, micro, micron, mil, mile, milli, minute, mmHg
from .constants import monster, mph, mu_0, nan, nanj, nano, nautical_mile, neg_inf, neg_infj, neutron_mass, ounce, oz
from .constants import parsec, pebi, peta, phi, phi_, pi, pico, point, pound, pound_force, proton_mass, psi, pt, rho
from .constants import short_ton, sigma, slinch, slug, speed_of_light, speed_of_sound, stone, supergoldenpsi, survey_foot
from .constants import survey_mile, tau, tebi, tera, ton_TNT, torr, troy_ounce, troy_pound, u, week, yard, year, yobi
from .constants import yotta, zebi, zepto, zero_Celsius, zetta, κ, π, ρ, τ, φ, φ_, ψ
from .mathfuncs import S, acos, acosh, acot, acoth, acsc, acsch, asec, asech, asin, asinh, atan, atan2, atanh
from .mathfuncs import binomial_coeficient, cas_variable, cbrt, ceil, cis, cos, cosh, cot, coth, csc, csch, cube, exp
from .mathfuncs import expm1, floor, from_str, icbrt, is_constant, isqrt, ln, log, log1p, log2, mathfunc, mathfunction
from .mathfuncs import polynomial, sec, sech, sigmoid, sin, sinh, sqrt, square, tan, tanh, tesser, x, y, z
from .nmath import AngleType, Composite, Factor, Heron, LawofCos, LawofSin, Prime, TriangleType, acute, circle
from .nmath import digit_prod, digit_sum, dist, equilateral, even, factorial, gcd, hypot, isTriangle, isclose, isfinite
from .nmath import isinf, isnan, isosceles, lcm, obtuse, odd, persistance, persistance_generator, phase, polar, triangle
from .nmath import primes_till, prod, product, rect, right, rt, scalene, segmented_sieve, sieve, straight, summation
from .basenum import fromNumBaseFormat, basenum
from .quaternion import quaternion, i, j, k
from .vector import vector, matrix
from .intervals import Interval, interval, unified_interval, is_interval

# eof
