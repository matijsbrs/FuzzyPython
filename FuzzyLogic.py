# Fuzzy Logic test
# Author: ing. M. Behrens
# Date: 11022021
# 
#

import json

class FuzzyPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Interpolate:
    def Linear(self,x, x0, y0, x1, y1):
        return y0 + ((x - x0) * ((y1 - y0) / (x1 - x0)))
    
    def Between(self, x, Point0, Point1):
        return self.Linear(x,Point0.x, Point0.y,Point1.x, Point1.y)

class Cluster:
    def __init__(self,Name):
        self.Sets = {}
        self.Name = Name
        self.Value = 0

    def loadFromJSON(self, jsonString, exclude = None):
        dataset = json.loads(jsonString)
        self.Name = dataset['Cluster']['Name']

        for item in dataset['Cluster']['Sets']:
            Name = item['Name']
            try:
                if Name in exclude:
                    # print("Excluded:", Name)
                    continue    
            except:
                pass
            subSet = Set(item['Name'])
            for point in item['Points']:
                subSet.AddPoint(point['x'],point['y'])
            self.append(subSet)

    def loadFromFile(self, filename, exclude = None):
        file = open(filename, "r")
        self.loadFromJSON(file.read(),exclude)

    def append(self, FuzzySet):
        self.Sets[FuzzySet.Name] = FuzzySet
    
    def get(self,name):
        return self.Sets[name]

    def Input(self, Value):
        self.InputValue = Value
        for Fuzzyset in self.Sets.values():
            Fuzzyset.Input(self.InputValue)

    def ListWeights(self):
        output = "Input Value: " + str(self.InputValue)
        for Fuzzyset in self.Sets.values():
            output += "" + Fuzzyset.Name + " : " + str(Fuzzyset.Weight())
        return output

    def ListAll(self):
        output = "Input Value: " + str(self.InputValue)
        for Fuzzyset in self.Sets.values():
            output += "" + Fuzzyset.Name + " : " + str(Fuzzyset.DOM )
        return output

    def GetProminent(self):
        output = ""
        maxValue = 0.0

        for Fuzzyset in self.Sets.values():
            if Fuzzyset.DOM > maxValue:
                maxValue = Fuzzyset
                output = Fuzzyset.Name
        return output
    
    # Singleton 
    def Sugeno(self):
        output = 0.0
        Upper = 0.0
        Lower = 0.0

        for Fuzzyset in self.Sets.values():
            print(Fuzzyset.Name, ":", Fuzzyset.Dom, " U:", Upper, " L:", Lower)
            if Fuzzyset.Dom > 0:
                Upper += Fuzzyset.Dom * Fuzzyset.WorkValue
                Lower += Fuzzyset.Dom
        if (Upper > 0) & (Lower > 0):
            output = Upper/Lower

        return output

    # Centre of gravity Calculation
    # mamdani method
    def Mamdani_original(self):
        output = 0.0
        UpperSum = 0.0
        LowerSum = 0.0

        for Fuzzyset in self.Sets.values():
            UpperSum += Fuzzyset.UpperSum()
            LowerSum += Fuzzyset.LowerSum()
        if ( UpperSum > 0 ) & (LowerSum > 0):
            # print("sum", UpperSum, " lSum:", LowerSum, " output:" , (UpperSum/LowerSum))
            output = UpperSum/LowerSum
        return output
    
    def Mamdani(self):
        output = 0.0
        UpperSum = 0.0
        LowerSum = 0.0

        for Fuzzyset in self.Sets.values():
            if Fuzzyset.Consequent > 0:
                UpperSum += (Fuzzyset.Sum() * Fuzzyset.Consequent )
                LowerSum += Fuzzyset.Consequent * len(Fuzzyset.Points)
        if ( UpperSum > 0 ) & (LowerSum > 0):
            # print(UpperSum, " lSum:", LowerSum, " output:" , (UpperSum/LowerSum))
            output = UpperSum/LowerSum
        
        return output

    def ToCrisp(self):
        return self.Mamdani()
        # return self.Sugeno()


class Set:
    def __init__(self,Name):
        self.Points = []
        self.Name = Name
        self.WorkValue = 0.0
        self.Dom = 0.0
        self.Consequent = 0.0
        self.Interpolater = Interpolate()

    def __and__(self, other):
        result = Set(self.Name + "&" + other.Name)
        result.Dom = min(self.Dom, other.Dom)
        return result

    def __or__(self, other):
        result = Set(self.Name + "|" + other.Name)
        result.Dom = max(self.Dom, other.Dom)
        return result

    def __add__(self, other):
        result = Set(self.Name + "+" + other.Name)
        result.Dom = min(1, (self.Dom + other.Dom))
        # print("add",result.Name, " ", self.Dom, " + ", other.Dom, "=",result.Dom)
        return result

    def __invert__(self):
        result = Set("!" + self.Name)
        result.Dom = 1 - self.Dom
        return result

    def AddPoint(self,x,y):
        self.Points.append(FuzzyPoint(x,y))
        self.Points.sort(key=lambda xVal: xVal.x, reverse=False)

    def Input(self, value):
        self.WorkValue = value
        self.CalculateDom()
        return self.WorkValue
    
    def Evaluate(self, value):
        self.Consequent = value
        return self.Consequent

    def Sum(self):
        output = 0.0
        for pt in self.Points:
            output += pt.x
        return output
    
    def UpperSum(self):
        output = 0.0
        for pt in self.Points:
            output += pt.x * min(pt.y, self.Dom)
        return output
    
    def LowerSum(self):
        output = 0.0
        for pt in self.Points:
            output += min(pt.y, self.Dom)
        return output

    def CalculateDom(self):
        output = 0.0
        if  len(self.Points) > 0 :
            if self.WorkValue > self.Points[-1].x:
                output = 0
                self.Dom = output
                return self.Dom
            elif self.WorkValue < self.Points[0].x:
                output = 0
                self.Dom = output
                return self.Dom
        previous = self.Points[0]
        for pt in self.Points:
            if self.WorkValue >= pt.x:
                previous = pt
            elif self.WorkValue <= pt.x:
                if previous == pt:
                    return output
                output = self.Interpolater.Between(self.WorkValue, previous, pt)
                self.Dom = output
                return output

        self.Dom = output
        return output


# Cluster = FuzzyCluster("Temperatuur")

# subSet = FuzzySet("Koud")
# subSet.AddPoint(0,1)
# subSet.AddPoint(15,1)
# subSet.AddPoint(20,0)
# Cluster.append(subSet)

# subSet = FuzzySet("Warm")
# subSet.AddPoint(15,0)
# subSet.AddPoint(20,1)
# subSet.AddPoint(24,0)
# Cluster.append(subSet)


# TempIn = 19.1
# Cluster.Input(TempIn)

# [print(item.Name, " DOM:", item.Dom ) for item in Cluster.Sets.values() ]



# Koud = FuzzySet("Koud")
# Warm = FuzzySet("Warm")

# Koud.AddPoint(0,1)
# Koud.AddPoint(15,1)
# Koud.AddPoint(20,0)

# Warm.AddPoint(15,0)
# Warm.AddPoint(20,1)
# Warm.AddPoint(24,0)


# Koud.Input(TempIn)
# Warm.Input(TempIn)
# print(" Koud.DOM     :" + str(Koud.Dom))
# print(" Warm.DOM     :" + str(Warm.Dom))
# print(" Warm&Koud.DOM:" + str( (Warm&Koud).Dom ))
# print(" Warm|Koud.DOM:" + str( (Warm|Koud).Dom ))

