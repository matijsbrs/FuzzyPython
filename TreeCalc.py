from os import get_inheritable
import re

ruleLine = "long+(short+extended_a)"
rules = ["1*2+c*d"]

rule = re.split(r"(\W)",ruleLine)

class Expr:
    pass

class Times(Expr) :
    def __init__(self, l,r):
        self.l = l
        self.r = r
    
    def __str__(self):
        return "(" + str(self.l) + "*" + str(self.r) + ")"

    def eval(self, env):
        return self.l.eval(env) * self.r.eval(env)

class Add(Expr) :
    def __init__(self, l,r):
        self.l = l
        self.r = r
    
    def __str__(self):
        return "(" + str(self.l) + "+" + str(self.r) + ")"

    def eval(self, env):
        return self.l.eval(env) + self.r.eval(env)

class Const (Expr):
    def __init__(self,val):
        self.val = val

    def __str__(self) :
        return str(self.val)

    def eval(self,env):
        return self.val

class Var (Expr):
    def __init__(self,name) :
        self.name = name
    
    def __str__(self) :
        return self.name

    def eval(self, env):
        return env[self.name]

def isExpr(field) :
    if re.search("[\+\-\*\:\|\&\!\^]", field) :
        return True
    return False

def isVar(field) :
    if re.search("^[a-zA-Z]", field) and not isExpr(field) : 
        return True
    return False

def isConst(field):
    if re.search("^([-+]|[0-9])", field) and not isExpr(field) : 
        return True
    return False

def FindExpr(s, start = 0 , end = 0, depth = 0):
    expressions = ['+','-','*',':','|','&']
    brackets = ['(',')']
    pos = 0
    for expr in s:
        left  = s[:pos]
        right = s[pos+1:]
        opr   = s[pos:pos+1]

        if expr in expressions:
            
            
            RIsVar      = isVar(right)
            RIsConst    = isConst(right)
            RIsExpr     = isExpr(right)

            LIsVar      = isVar(left)
            LIsConst    = isConst(left)
            LIsExpr     = isExpr(left)


            print("%")
            print(" Opr:{}\t".format(opr))
            print(" lft:{}\tv{}\tc{}\te{}".format(left,isVar(left),isConst(left),isExpr(left)))
            print(" rgt:{}\tv{}\tc{}\te{}".format(right,isVar(right),isConst(right),isExpr(right)))
            

            Raction = ""
            if RIsVar:
                Raction = "Var({})".format(right)
            elif RIsConst:
                Raction = "Const({})".format(right)
            elif RIsExpr:
                # Raction = FindExpr(right)
                right = FindExpr(right)
                Raction = "{}".format(right)
                # start nesting from here. 

            Laction = ""
            if LIsVar:
                # Laction = Var(left)
                Laction = "Var({})".format(left)
            elif LIsConst:
                # Laction = Const(left)
                Laction = "Const({})".format(left)
            elif LIsExpr:
                # Laction = FindExpr(left)
                left = FindExpr(left)
                Laction = "Expr({})".format(left)
                # start nesting from here. 
            

            action = ""
            if opr == "*":
                action = "Times({},{})".format(Laction,Raction)
                # action = Times(Laction,Raction)
            elif opr == "+":
                action = "Add({},{})".format(Laction,Raction)
                # action = Add(Laction,Raction)
           
           
            # print(FindExpr(right))

            # print("E:{}\t L:{} \t R:{} ".format(opr,left,right))
            
            return action

        elif expr in brackets:
            if expr == "(" :
                depth += 1
            else :
                depth -= 1
            
            print("*"*(depth))
            return FindExpr(s[pos+1:],depth=depth)
           

        pos += 1


env = { "a" : 2, "b" : 4, "c" : 5, "d" : 3}
for s in rules:
    # print("s:'{}'\t\t -> {}".format(s,getBrackets(s)))
    print("s:'{}'\t\t -> {}".format(s,FindExpr(s) ))
    # print("{}: {}".format(s,rulesplit(s)))
    # print(parts)
    print("---")

# calculator example:
# env = { "x" : 2, "y" : 4, "z" : 2}
# e1 = Times(Var("z"), Add(Var("y"),Var("x")) )
# print(e1)