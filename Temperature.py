# Fuzzy Logic test
# Author: ing. M. Behrens
# Date: 11022021

import FuzzyLogic
import json


Cluster = FuzzyLogic.Cluster("")
Cluster.loadFromFile("./Fuzzy/Temperature.json")

TempIn = -1
Cluster.Input(TempIn)

Stoken = Cluster.get('Erg koud')|Cluster.get('Vorst')
print ( "Stoken: ", Stoken.Dom)

[print(item.Name, " DOM:", item.Dom ) for item in Cluster.Sets.values() ]
