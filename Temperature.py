# Fuzzy Logic test
# Author: ing. M. Behrens
# Date: 11022021

import FuzzyLogic
import json

CV = FuzzyLogic.Cluster("")
CV.loadFromFile("./Stooklijn.json", exclude="Wind")

CVComp = FuzzyLogic.Cluster("")
CVComp.loadFromFile("./Stooklijn.json",exclude=['Hoog','Laag'])

Wind = FuzzyLogic.Cluster("")
Wind.loadFromFile("./Wind.json")

Cluster = FuzzyLogic.Cluster("")
Cluster.loadFromFile("./Temperatures.2.json")

WindSnelheid = 4.9 # Meter / sec

for TempIn in range(-9,21,3):
    Cluster.Input(TempIn)
    
    StokenHoog = Cluster.get('Koud')
    StokenLaag = Cluster.get('Warm')
    
    CV.get('Hoog').Evaluate(StokenHoog.Dom)
    CV.get('Laag').Evaluate(StokenLaag.Dom)
    
    print (  "T: ", TempIn, "\tLow:", round(StokenLaag.Dom,2)," \tHigh:", round(StokenHoog.Dom,2) )
    # [print(item.Name, " DOM:", item.Dom ) for item in Cluster.Sets.values() ]
    print ( "T: ", TempIn, "\t CV: ", round(CV.ToCrisp(),2), "\t Final advice:", round(CV.ToCrisp(),2) )
    # [print(item.Name, " DOM:", item.Dom ) for item in Wind.Sets.values() ]
    # print ("")


# [print(item.Name, " DOM:", item.Dom ) for item in Wind.Sets.values() ]

# for WindSnelheid in range (0,5):
#     Wind.Input(WindSnelheid)

#     WindComp = Wind.get('Wind5')
#     CVComp.get('Wind').Input(WindComp.Dom)
#     print("Ws:",WindSnelheid, " \tWindComp: ", WindComp.Dom, " comp:", CVComp.ToCrisp())