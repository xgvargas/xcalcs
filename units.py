# -*- coding: utf-8 -*-

from PySide import QtCore

class Converter(QtCore.QObject):

    def __init__(self):
        super().__init__()

        self.units = {

# aceleracao
# centimeter per second squared   cm/s2   meter per second squared    0.01
# foot per hour per second    ft/(h·s)    meter per second squared    8.46667E-05
# foot per minute per second  ft/(min·s)  meter per second squared    0.00508
# foot per second squared ft/s2   meter per second squared    0.3048
# galileo Gal meter per second squared    0.01
# gravity (standard)  gn  meter per second squared    9.80665
# inch per hour per second    in/(h·s)    meter per second squared    7.05556E-06
# inch per minute per second  in/(min·s)  meter per second squared    4.23333E-04
# inch per second squared in/s2   meter per second squared    0.0254
# meter per second squared    m/s2    meter per second squared    1
# knot per second kn/s    meter per second squared    0.5144444
# mile per hour per second    mi/(h·s)    meter per second squared    0.44704
# mile per minute per second  mi/(min·s)  meter per second squared    26.8244
# mile per second squared mi/s2   meter per second squared    1609.344

#densidade
# gram per cubic centimeter   g/cm3   kilogram per cubic meter    1000
# kilogram per cubic centimeter   kg/cm3  kilogram per cubic meter    1000000
# gram per cubic meter    g/m3    kilogram per cubic meter    0.001
# kilogram per cubic meter    kg/m3   kilogram per cubic meter    1
# gram per milliliter g/mL    kilogram per cubic meter    1000
# gram per liter  g/L kilogram per cubic meter    1
# kilogram per liter  kg/L    kilogram per cubic meter    1000
# ounce per cubic inch    oz/in3  kilogram per cubic meter    1729.994
# ounce per cubic foot    oz/ft3  kilogram per cubic meter    1.001153
# pound per cubic inch    lb/in3  kilogram per cubic meter    27679.90471
# pound per cubic foot    lb/ft3  kilogram per cubic meter    16.018463
# ounce per gallon (Imperial) oz/gal  kilogram per cubic meter    6.236023
# ounce per gallon (U.S. fluid)   oz/gal  kilogram per cubic meter    7.489151
# pound per gallon (Imperial) lb/gal  kilogram per cubic meter    99.776372
# pound per gallon (U.S. fluid)   lb/gal  kilogram per cubic meter    119.826
# slug per cubic foot slug/ft3    kilogram per cubic meter    515.3788184
# ton per cubic yard (long)   l ton/yd3   kilogram per cubic meter    1328.939
# ton per cubic yard (short)  sh ton/yd3  kilogram per cubic meter    1186.553

#time
# nanosecond  ns  second  0.000000001
# millisecond ms  second  0.001
# second  s   second  1
# second (sidereal)   s   second  0.99726956
# minute  min second  60
# minute (sidereal)   min second  59.83617361
# hour    h   second  3600
# hour (sidereal) h   second  3590.170417
# day d   second  86400
# day (sidereal)  d   second  86164.09
# week    wk  second  604800
# month   mo  second  2628000
# shake   shake   second  0.00000001
# year    yr  second  31536000
# year (sidereal) yr  second  31449892.85
# decade  dec second  315360000
# century c   second  3153600000
# millennium  millennium  second  31536000000
            0: [ # angle
                (self.tr('degrees'), '', 3600),
                (self.tr('gradians'), '', 3240),
                (self.tr('minute'), '', 60),
                (self.tr('rad'), '', 206265),
                (self.tr('revolution'), '', 1296000),
                (self.tr('straight'), '', 324000),
                (self.tr('second'), '', 1),
# radian  rad degree  180/π   57.29578    radian  1   1
# degree  °   degree  1   1   radian  π/180   0.01745329
# minutes '   degree  1/60    0.016667    radian  (π/180)/60  2.908882e-04
# seconds "   degree  1/3600  2.777778e-4 radian  (π/180)/3600    4.848137e-06
# octant  octant  degree  360/8   45  radian  2π/8    0.7853982
# sextant sextant degree  360/6   60  radian  2π/6    1.047196
# quadrant    quadrant    degree  360/4   90  radian  2π/4    1.570796
# revolution  r   degree  360/1   360 radian  2π  6.283185
# gon gon degree  360/400 0.9 radian  2π/400  0.01570796
# mil mil degree  360/6400    0.05625 radian  2π/6400 9.817477e-4
                ],
            1: [ # area
                (self.tr('square inch'), 'in2', 0.00064516),
                (self.tr('square foot'), 'ft2', 0.09290304),
                (self.tr('square yard'), 'yd2', 0.83612736),
                (self.tr('square mile'), 'mi2', 2589988.110336),
                (self.tr('acre'), 'ac', 4046.8564224),
                (self.tr('hectare'), 'ha', 10000),
                (self.tr('square millimeter'), 'mm2', 0.000001),
                (self.tr('square centimeter'), 'cm2', 0.0001),
                (self.tr('square meter'), 'm2', 1),
                (self.tr('square kilometer'), 'km2', 1000000),
                ],
            2: [ # dimension
                (self.tr('mil'), 'mil', 0.0000254),
                (self.tr('inch'), 'in', 0.0254),
                (self.tr('foot'), 'ft', 0.3048),
                (self.tr('yard'), 'yd', 0.9144),
                (self.tr('mile'), 'mi', 1609.344),
                (self.tr('capefoot'), 'cf', 0.314856),
                (self.tr('rod'), 'rd', 5.0292),
                (self.tr('angstrom'), 'Å', 1E-10),
                (self.tr('nanometer'), 'n', 0.000000001),
                (self.tr('micron'), 'µ', 0.000001),
                (self.tr('millimeter'), 'mm', 0.001),
                (self.tr('centimeter'), 'cm', 0.01),
                (self.tr('meter'), 'm', 1),
                (self.tr('kilometer'), 'km', 1000),
                (self.tr('light-year'), 'l.y', 9460730472580800),
                (self.tr('light-day'), '', 25902068371200),
                (self.tr('light-hour'), '', 1079252848800),
                (self.tr('light-minute'), '', 17987547480),
                (self.tr('light-second'), '', 299792458),
                ],
            3: [ # energy
                (self.tr('joule'), 'J', 1),
                (self.tr('watt-second'), 'Ws', 1),
                (self.tr('watt-hour'), 'Wh', 3600),
                (self.tr('kWatt-hour'), 'kWh', 3600000),
                (self.tr('calory'), 'cal', 4.1868),
                (self.tr('BTU'), '', 1055.056),
                (self.tr('Nm'), '', 1),
# British thermal unit [IT]   BTUIT   joule   1055.056
# British thermal unit [th]   BTUth   joule   1054.35
# British thermal unit [mean] BTUmean joule   1055.87
# British thermal unit [39°F] BTU39°F joule   1059.67
# British thermal unit [59°F] BTU59°F joule   1054.8
# British thermal unit [60°F] BTU60°F joule   1054.68
# calorie [IT]    calIT   joule   4.1868
# calorie [th]    calth   joule   4.184
# calorie [mean]  calmean joule   4.19002
# calorie [15°C]  cal15°C joule   4.1858
# calorie [20°C]  cal20°C joule   4.1819
# electronvolt    eV  joule   1.60218E-19
# erg erg joule   0.0000001
# foot-poundal    ft·pdl  joule   0.04214011
# foot-pound-force    ft·lbf  joule   1.355818
# inch-pound-force    in·lbf  joule   0.112984829
# joule   J   joule   1
# megajoule   MJ  joule   1000000
# kilocalorie [IT]    kcalIT  joule   4186.8
# kilocalorie [th]    kcalth  joule   4184
# kilocalorie [mean]  kcalmean    joule   4190.02
# kilowatt-hour   kW·h    joule   3600000
# quad (IT)   quad    joule   1.05506E+18
# therm (EC)  therm   joule   105506000
# therm (U.S.)    therm   joule   105480400
# ton-of-coal-equivalent  TOC joule   29307600000
# ton-of-oil-equivalent   TOE joule   41868000000
# ton-of-TNT-equivalent   tTNT    joule   4184000000
# watt-hour   W·h joule   3600
# watt-second W·s joule   1
                ],
            4: [ # flux
                (self.tr(''), '', ),
                ],
            5: [ # force
                (self.tr('dyne'), 'dyn', 0.00001),
                (self.tr('kilogram-force'), 'kgf', 9.80665),
                (self.tr('kilopond'), 'kp', 9.80665),
                (self.tr('kip'), 'kip', 4448.222),
                (self.tr('newton'), 'N', 1),
                (self.tr('kilonewton'), 'kN', 1000),
                (self.tr('ounce-force'), 'ozf', 0.2780139),
                (self.tr('poundal'), 'pdl', 0.138255),
                (self.tr('pound-force'), 'lbf', 4.448222),
                (self.tr('ton-force'), 'tnf', 8896.443),
                ],
            6: [ # mass
                (self.tr('gram'), 'g', 1),
                (self.tr('kilogram'), 'kg', 1000),
                (self.tr('pound'), '', 373.2417),
                (self.tr('ounce'), '', 28.34952),
                (self.tr('libre'), 'lb', 453.5924),
                (self.tr('grain'), '', .0648),
                (self.tr('ton'), '', 1000000),
# carat (metric)  ct  gram    0.2
# point (metric)  pt  gram    0.002
# dram (avdp) dr  gram    1.771845195
# dram (troy) dr  gram    3.8879346
# grain (metric)  gr  gram    0.05
# grain (troy)    gr  gram    0.06479891
# gram    g   gram    1
# hundredweight (long)    hwt gram    50802.34544
# hundredweight (short)   hwt gram    45359.237
# kilogram    kg  gram    1000
# megagram    Mg  gram    1000000
# milligram   mg  gram    0.001
# ounce (avdp)    oz  gram    28.34952313
# ounce (troy)    oz  gram    31.1034768
# pennyweight dwt gram    1.55517384
# pound (avdp)    lb  gram    453.59237
# pound (metric)  lb  gram    500
# pound (troy)    lb  gram    373.2417216
# slug    slug    gram    14593.903
# stone   st  gram    6350.29318
# ton-assay (long)    l AT    gram    32.666667
# ton-assay (short)   sh AT   gram    29.166667
# ton (long)  l tn    gram    1016046.909
# ton (short) sh tn   gram    907184.74
# ton-metric  t   gram    1000000
# tonne (U.S. metric ton) t   gram    1000000
                ],
            7: [ # power
                (self.tr(''), '', ),
# BTU [IT] per hour   BTUIT/h watt    0.2930711
# BTU [IT] per minute BTUIT/min   watt    0.2930711*60
# BTU [IT] per second BTUIT/s watt    0.2930711*60*60
# calorie [IT] per hour   calIT/h watt    4.1868/60/60
# calorie [IT] per minute calIT/min   watt    4.1868/60
# calorie [IT] per second calIT/sec   watt    4.1868
# BTU [th] per hour   BTUth/h watt    0.2928751
# BTU [th] per minute BTUth/min   watt    0.2928751*60
# BTU [th] per second BTUth/s watt    0.2928751*60*60
# calorie [th] per hour   calth/h watt    4.184/60/60
# calorie [th] per minute calth/min   watt    4.184/60
# calorie [th] per second calth/s watt    4.184
# cheval-vapeur   cv  watt    735.49875
# erg per hour    erg/h   watt    0.0000001/60/60
# erg per minute  erg/min watt    0.0000001/60
# erg per second  erg/s   watt    0.0000001
# foot-pound-force per hour   ft·lbf/h    watt    1.355818/60/60
# foot-pound-force per minute ft·lbf/min  watt    1.355818/60
# foot-pound-force per second ft·lbf/s    watt    1.355818
# foot-poundal per hour   ft·pdl/h    watt    0.04214011/60/60
# foot-poundal per minute ft·pdl/min  watt    0.04214011/60
# foot-poundal per second ft·pdl/s    watt    0.04214011
# horsepower (550 ft � lbf/s) hp  watt    745.6999
# horsepower (boiler) hp  watt    9809.5
# horsepower (electric)   hp  watt    746
# horsepower (metric) hp  watt    735.49875
# horsepower (U.K.)   hp  watt    745.7
# horsepower (water)  hp  watt    746.043
# joule per hour  J/h watt    1/60/60
# joule per minute    J/min   watt    1/60
# joule per second    J/s watt    1
# kilowatt    kW  watt    1000
# pferdestarke    PS  watt    735.49875
# watt    W   watt    1

                ],
            8: [ # speed
                (self.tr('km/h'), '', .277777777777),
                (self.tr('m/s'), '', 1),
                (self.tr('mi/h'), '', .44704),
# centimeter per minute   cm/min  meter per second    0.0001667
# centimeter per second   cm/s    meter per second    0.01
# foot per hour   ft/h    meter per second    8.46667E-05
# foot per minute ft/min  meter per second    0.00508
# foot per second ft/s    meter per second    0.3048
# inch per minute in/min  meter per second    0.000423333
# inch per second in/s    meter per second    0.0254
# kilometer per hour  km/h (kph)  meter per second    0.2777778
# kilometer per second    km/s    meter per second    1000
# knot (nautical mi/h)    kn  meter per second    0.5144444
# knot (UK)   kn  meter per second    0.5148
# meter per hour  m/h meter per second    0.0002777778
# meter per minute    m/min   meter per second    0.01667
# meter per second    m/s meter per second    1
# mile per hour   mi/h (mph)  meter per second    0.44704
# mile per minute mi/min  meter per second    26.8224
# mile per second mi/s    meter per second    1609.344
# speed-of-light (vacuum) c   meter per second    299792458
# yard per hour   yd/h    meter per second    0.000254
# yard per minute yd/min  meter per second    0.01524
# yard per second yd/s    meter per second    0.9144
                ],
            9: [ # pressure
                (self.tr('bar'), '', 100000),
                (self.tr('atm'), '', 101325),
                (self.tr('psi'), '', 6894.757),
                (self.tr('torr'), '', 133.3224),
                (self.tr('pascal'), '', 1),
                (self.tr('cmHg'), '', 1333.22),
                (self.tr('cmH2O'), '', 98.0638),
# atmosphere-standard atm pascal  101325
# atmosphere-technical    at  pascal  98066.5
# bar bar pascal  100000
# decibar dbar    pascal  1000
# millibar    mbar    pascal  100
# barye (cgs unit)    barye   pascal  0.1
# centimeter of mercury   cmHg    pascal  1333.22
# centimeter of water (4 °C)  cmH2O   pascal  98.0638
# foot of mercury (conventional)  ftHg    pascal  40636.66
# foot of water (39.2 °F) ftH2O   pascal  2988.98
# inch of mercury (conventional)  inHg    pascal  3386.389
# inch of water (39.2 °F) inH2O   pascal  248.082
# kilogram-force per square millimeter    kgf/mm2 pascal  9806650
# kip per square inch kip/in2 pascal  6894757
# millimeter of mercury   mmHg    pascal  133.3224
# millimeter of water (3.98 °C)   mmH2O   pascal  9.80638
# pascal  Pa  pascal  1
# hectopascal hPa pascal  100
# kilopascal  kPa pascal  1000
# pound per square foot   lb/ft2  pascal  47.88025
# pound per square inch   lb/in2 or psi   pascal  6894.757
# poundal per square foot pdl/ft2 pascal  1.488164
# short ton per square foot   sh tn/ft2   pascal  95760.518
# torr    torr    pascal  133.3224
                ],
            10: [ # temperature
                (self.tr('celsius'), '', 0),
                (self.tr('kelvin'), '', 0),
                (self.tr('fahrenheit'), '', 0),
                (self.tr('réaumur'), '', 0),
                (self.tr('rankine'), '', 0),
                ],
            11: [ # volume
                (self.tr('l'), '', 1),
                (self.tr('gal'), '', 3.7854),
                (self.tr('m^3'), '', 1000),
# acre-foot   ac ft   cubic meter 1233.481838
# barrel (Imperial)   bl  cubic meter 0.16365924
# barrel (petroleum)  bl  cubic meter 0.158987295
# barrel (U.S. dry)   bl  cubic meter 0.115628199
# barrel (U.S. fluid) bl  cubic meter 0.119240471
# bushel (Imperial)   bu  cubic meter 0.03636872
# bushel (U.S. dry)   bu  cubic meter 0.03523907
# cord (firewood) cord    cubic meter 3.624556364
# cubic foot  ft3 cubic meter 0.028316847
# cubic inch  in3 cubic meter 1.63871E-05
# cubic centimeter    cm3 cubic meter 0.000001
# cubic meter m3  cubic meter 1
# cubic mile  mi3 cubic meter 4168181825
# cubic yard  yd3 cubic meter 0.764554858
# cup (breakfast) c   cubic meter 0.000284131
# cup (Canadian)  c   cubic meter 0.000227305
# cup (U.S.)  c   cubic meter 0.000236588
# ounce (Imperial fluid)  oz  cubic meter 2.84131E-05
# ounce (U.S. fluid)  oz  cubic meter 2.95735E-05
# gallon (Imperial)   gal cubic meter 0.00454609
# gallon (U.S. dry)   gal cubic meter 0.004404884
# gallon (U.S. fluid) gal cubic meter 0.003785412
# gill (Imperial) gi  cubic meter 0.000142065
# gill (U.S.) gi  cubic meter 0.000118294
# hogshead (Imperial) hhd cubic meter 0.32731848
# hogshead (U.S.) hhd cubic meter 0.238480942
# liter   L   cubic meter 0.001
# milliliter  mL  cubic meter 0.000001
# peck (Imperial) pk  cubic meter 0.00909218
# peck (U.S. dry) pk  cubic meter 0.008809768
# pint (Imperial) pt  cubic meter 0.000568261
# pint (U.S. dry) pt  cubic meter 0.00055061
# pint (U.S. fluid)   pt  cubic meter 0.000473176
# quart (Imperial)    qt  cubic meter 0.001136523
# quart (U.S. dry)    qt  cubic meter 0.001101221
# quart (U.S. fluid)  qt  cubic meter 0.000946353
# tablespoon (Canadian)   tbsp    cubic meter 1.42065E-05
# tablespoon (Imperial)   tbsp    cubic meter 1.77582E-05
# tablespoon (U.S.)   tbsp    cubic meter 1.47868E-05
# teaspoon (Canadian) tsp cubic meter 4.73551E-06
# teaspoon (Imperial) tsp cubic meter 5.91939E-06
# teaspoon (U.S.) tsp cubic meter 4.92892E-06
                ],
            }

    def getNames(self, index):
        l = []
        for n in self.units[index]:
            l.append(n[0])
        return l

    def convert(self, val, index, from_idx, to_idx):

        if index == 10:  # temperature
            # C/100 = (K-273.15)/100 = (F-32)/180 = R/80 = ((Rankine/1.8)-273.15)/100

            if from_idx == 0: tmp = val/100
            elif from_idx == 1: tmp = (val-273.15)/100
            elif from_idx == 2: tmp = (val-32)/180
            elif from_idx == 3: tmp = val/80
            elif from_idx == 4: tmp = (val/1.8-273.15)/100

            if to_idx == 0: out = tmp*100
            elif to_idx == 1: out = tmp*100+273.15
            elif to_idx == 2: out = tmp*180+32
            elif to_idx == 3: out = tmp*80
            elif to_idx == 4: out = (tmp*100+273.15)*1.8
        else:
            out = val*self.units[index][from_idx][2]/self.units[index][to_idx][2]

        return out, self.units[index][to_idx][1]
