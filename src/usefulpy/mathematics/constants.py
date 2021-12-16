'''
Constants

DESCRIPTION
Stores constants for mathematical calculation.

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Stores constants for mathematical calculation.
'''


inf = float('inf')
neg_inf = -inf
infj = complex('infj')
neg_infj = -infj
nanj = complex('nanj')
nan = float('nan')


### Non-Algebraic Numbers ###

# way more digits than it will store... so the most accurate possible
# I originially had it be calculated with formulae, (averaging the leibniz
# and basil approach with odd numbers for pi) but I decided that this
# was more efficient and more accurate (I kept on adjusting the numbers to get
# a bit more accuracy, but I still wasn't quite happy with it.

# e, number where f(x)=e^x, its derivative, f'(x) also equals e^x
e = 2.71828182845904523536028747135266249775724709369995957496  # ...
# π, ratio of diameter to circumference in circle
π = pi = 3.141592653589793238462643383279502884197169399375105  # ...
# τ, ratio of diameter to circumference in circle
τ = tau = 2*pi

### Algebraic numbers ###

# φ
#
# 1/(1+1/(1+1/(1+1/(1+1/(1+1/(1+1/(1+1/(1+1/(...)))))))))
# φ-1 = 1/φ, φ**2-φ = 1, φ**2-φ-1 = 0, etc.
# also (a+a*Φ)/a*Φ = a/a*Φ, golden ratio
#
# pops up everywhere
# for example, a math problem I did recently:
#
# f'(x) = f^-1(x)
# If you try to find a solution in the form
# f(x) = a(x**r)
# then f'(x) = (x**(r-1))
# and f^-1(x) = ((1/a)**(1/r))*(x**(1/r))
# if the equations will be equal, the power of x has to be equal, so
# (x**(r-1)) = (x**(1/r))
# (r-1) = (1/r) # No need to go any further, this is a definition of φ
# r = φ, (or the radical conjugate of φ, which we will note as φ_)
# Thus:
# (1/a)**(1/φ_) = φ_*a and (1/a)**(1/φ) = ra
# or
# (1/a)**(1/r) = ra
# where r assumes the properties of φ and φ_
# (1/a)**(1/r) = ra
# (1/a)**(r-1) = ra   #property of φ
# a**(1-r) = ra
# a**r = r
# a = ^r√r # rth root of r, true for φ and φ_
#
# this means f'(x) = f^-1(x) when f(x) = (^φ√φ)*(x**φ) or (^φ_√φ_)*(x**φ_)
# let's check this (because I've gotten carried away)
# f'(x) = φ(φ^√(1/φ))*(x**(φ-1))
# f'(x) = φ(φ^√φ**-1)*(x**(1/φ))
# f'(x) = φ(φ^√φ**-1)*(^φ√x)
# f'(x) = ^φ√(φ**φ)(φ^√φ**-1)*(^φ√x)
# f'(x) = ^φ√((φ**φ)φ**-1)*(^φ√x)
# f'(x) = ^φ√((φ**(φ-1))*^φ√x
# f'(x) = ^φ√((φ**(1/φ))*^φ√x
#
# f'(x) = ^(φ**2)√φ * ^φ√x
#
# f^-1(x) = (1/^φ√(1/φ))**(1/φ) * φ**1/φ
# f^-1(x) = (1/^φ√(1/φ))**(1/φ) * ^φ√x
# f^-1(x) = (1/(1/φ**(1/φ)))**(1/φ) * ^φ√x
# f^-1(x) = (φ**(1/φ))**(1/φ) * ^φ√x
# f^-1(x) = φ**(1/φ**2) * ^φ√x
#
# f^-1(x) = ^(φ**2)√φ * ^φ√x
#
# f'(x) = ^(φ**2)√φ * ^φ√x, f^-1(x) = ^(φ**2)√φ * ^φ√x
# f'(x) = f^-1(x)
# Quod Erat Demonstratum!

_radical = 5**(1/2)
φ = phi = (1+_radical)/2
# radical conjugate of φ, same properties
φ_ = phi_ = (1-_radical)/2


# Bronze ratio, 3+1/(3+1/(3+1/(3+1/(3+1/(...)))))
_radical = 13**(1/2)
κ = kappa = (3+_radical)/2

# ρ**3 = ρ+1
_radical = 69**(1/2)
_a = (9+_radical)/18
_b = (9-_radical)/18
ρ = rho = _a**(1/3)+_b**(1/3)

# ψ, supergolden ratio x**3 = x**2+1
_radical = 93**(1/2)
_a = ((29+3*_radical)/2)**(1/3)
_b = ((29-3*_radical)/2)**(1/3)
_sum = (1+_a+_b)
ψ = supergoldenpsi = _sum/3

del _radical
del _sum

# Its a bit of a tongue twister, but: the number nicknamed monster is the
# Number of sets of symmetries in the largest finite group of sets of
# symmetries
monster = 808017424794512875886459904961710757005754368000000000


Avogadro = 6.02214076e+23
Boltzmann = 1.380649e-23
Btu = 1055.05585262
Btu_IT = 1055.05585262
Btu_th = 1054.3502644888888
G = 6.6743e-11
Julian_year = 31557600.0
N_A = 6.02214076e+23
Planck = 6.62607015e-34
R = 8.314462618
Rydberg = 10973731.56816
Stefan_Boltzmann = 5.670374419e-08
Wien = 0.002897771955
acre = 4046.8564223999992
alpha = 0.0072973525693
angstrom = 1e-10
arcmin = 0.0002908882086657216
arcminute = 0.0002908882086657216
arcsec = 4.84813681109536e-06
arcsecond = 4.84813681109536e-06
astronomical_unit = 149597870700.0
atm = 101325.0
atmosphere = 101325.0
atomic_mass = 1.6605390666e-27
atto = 1e-18
au = 149597870700.0
bar = 100000.0
barrel = 0.15898729492799998
bbl = 0.15898729492799998
blob = 175.12683524647636
c = 299792458.0
calorie = 4.184
calorie_IT = 4.1868
calorie_th = 4.184
carat = 0.0002
centi = 0.01
day = 86400.0
deci = 0.1
degree = 0.017453292519943295
degree_Fahrenheit = 0.5555555555555556
deka = 10.0
dyn = 1e-05
dyne = 1e-05
eV = 1.602176634e-19
electron_mass = 9.1093837015e-31
electron_volt = 1.602176634e-19
elementary_charge = 1.602176634e-19
epsilon_0 = 8.8541878128e-12
erg = 1e-07
exa = 1e+18
exbi = 1152921504606846976
femto = 1e-15
fermi = 1e-15
fine_structure = 0.0072973525693
fluid_ounce = 2.9573529562499998e-05
fluid_ounce_US = 2.9573529562499998e-05
fluid_ounce_imp = 2.84130625e-05
foot = 0.30479999999999996
g = 9.80665
gallon = 0.0037854117839999997
gallon_US = 0.0037854117839999997
gallon_imp = 0.00454609
gas_constant = 8.314462618
gibi = 1073741824
giga = 1000000000.0
golden = 1.618033988749895
golden_ratio = 1.618033988749895
grain = 6.479891e-05
gram = 0.001
gravitational_constant = 6.6743e-11
h = 6.62607015e-34
hbar = 1.0545718176461565e-34
hectare = 10000.0
hecto = 100.0
horsepower = 745.6998715822701
hour = 3600.0
hp = 745.6998715822701
inch = 0.0254
kgf = 9.80665
kibi = 1024
kilo = 1000.0
kilogram_force = 9.80665
kmh = 0.2777777777777778
knot = 0.5144444444444445
lb = 0.45359236999999997
lbf = 4.4482216152605
light_year = 9460730472580800.0
liter = 0.001
litre = 0.001
long_ton = 1016.0469088
m_e = 9.1093837015e-31
m_n = 1.67492749804e-27
m_p = 1.67262192369e-27
m_u = 1.6605390666e-27
mach = 340.5
mebi = 1048576
mega = 1000000.0
metric_ton = 1000.0
micro = 1e-06
micron = 1e-06
mil = 2.5399999999999997e-05
mile = 1609.3439999999998
milli = 0.001
minute = 60.0
mmHg = 133.32236842105263
mph = 0.44703999999999994
mu_0 = 1.25663706212e-06
nano = 1e-09
nautical_mile = 1852.0
neutron_mass = 1.67492749804e-27
ounce = 0.028349523124999998
oz = 0.028349523124999998
parsec = 3.085677581491367e+16
pebi = 1125899906842624
peta = 1000000000000000.0
pi = 3.141592653589793
pico = 1e-12
point = 0.00035277777777777776
pound = 0.45359236999999997
pound_force = 4.4482216152605
proton_mass = 1.67262192369e-27
psi = 6894.757293168361
pt = 0.00035277777777777776
short_ton = 907.1847399999999
sigma = 5.670374419e-08
slinch = 175.12683524647636
slug = 14.593902937206364
speed_of_light = 299792458.0
speed_of_sound = 340.5
stone = 6.3502931799999995
survey_foot = 0.3048006096012192
survey_mile = 1609.3472186944373
tau = 6.283185307179586
tebi = 1099511627776
tera = 1000000000000.0
ton_TNT = 4184000000.0
torr = 133.32236842105263
troy_ounce = 0.031103476799999998
troy_pound = 0.37324172159999996
u = 1.6605390666e-27
week = 604800.0
yard = 0.9143999999999999
year = 31536000.0
yobi = 1208925819614629174706176
yotta = 1e+24
zebi = 1180591620717411303424
zepto = 1e-21
zero_Celsius = 273.15
zetta = 1e+21
