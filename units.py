# -*- coding: utf-8 -*-

from PySide import QtCore

class Converter(QtCore.QObject):

    def __init__(self):
        super().__init__()

        self.units = {
            0: [ # angle
                (self.tr('degrees'), '', 3600),
                (self.tr('gradians'), '', 3240),
                (self.tr('minute'), '', 60),
                (self.tr('rad'), '', 206265),
                (self.tr('revolution'), '', 1296000),
                (self.tr('straight'), '', 324000),
                (self.tr('second'), '', 1),
                ],
            1: [ # area
                (self.tr(''), '', ),
                ],
            2: [ # dimension
                (self.tr('milimeter'), 'mm', 1.),
                (self.tr('centimeter'), 'cm', 10.),
                (self.tr('meter'), 'm', 1000.),
                (self.tr('inch'), 'in', 25.4),
                (self.tr('kilometer'), 'km', 1000000),
                (self.tr('mils'), 'mil', .0254),
                (self.tr('mile'), 'mi', 1609344),
                (self.tr('yard'), 'yd', 914.4),
                (self.tr('feet'), 'ft', 304.8),
                ],
            3: [ # energy
                (self.tr('joule'), 'J', 1),
                (self.tr('watt-second'), 'Ws', 1),
                (self.tr('watt-hour'), 'Wh', 3600),
                (self.tr('kWatt-hour'), 'kWh', 3600000),
                (self.tr('calory'), 'cal', 4.1868),
                (self.tr('BTU'), '', 1055.056),
                (self.tr('Nm'), '', 1),
                ],
            4: [ # flux
                (self.tr(''), '', ),
                ],
            5: [ # force
                (self.tr(''), '', ),
                ],
            6: [ # mass
                (self.tr('gram'), 'g', 1),
                (self.tr('kilogram'), 'kg', 1000),
                (self.tr('pound'), '', 373.2417),
                (self.tr('ounce'), '', 28.34952),
                (self.tr('libre'), 'lb', 453.5924),
                (self.tr('grain'), '', .0648),
                (self.tr('ton'), '', 1000000),
                ],
            7: [ # power
                (self.tr(''), '', ),
                ],
            8: [ # speed
                (self.tr('km/h'), '', .277777777777),
                (self.tr('m/s'), '', 1),
                (self.tr('mi/h'), '', .44704),
                ],
            9: [ # pressure
                (self.tr('bar'), '', 100000),
                (self.tr('atm'), '', 101325),
                (self.tr('psi'), '', 6894.757),
                (self.tr('torr'), '', 133.3224),
                (self.tr('pascal'), '', 1),
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
            elif to_idx ==1: out = tmp*100+273.15
            elif to_idx ==2: out = tmp*180+32
            elif to_idx ==3: out = tmp*80
            elif to_idx ==4: out = (tmp*100+273.15)*1.8
        else:
            out = val*self.units[index][from_idx][2]/self.units[index][to_idx][2]

        return out
