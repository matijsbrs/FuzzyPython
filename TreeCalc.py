from os import get_inheritable
import re



ruleLine = "long+(short+extended_a)"
rules = ["1*(2+(4+8))*10"]

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

def FindBracket(s,depth = 0, pos = 0, end = 0):
    brackets = ['(',')']
    start = -1
    pre = str(depth)*(depth+1)
    for pos in range(pos, len(s)):
        expr = s[pos]
        if expr in brackets:
            if expr == '(':
                if start < 0 : start = pos+1
                depth += 1
                print(pre, "\str:{}\t s:{}".format(start,s[start:]))
                # result = FindBracket(s,pos = pos+1, open = open, start = start)
                # print (pre, "result:" + result + " " + str(start) )
                # return result
            elif expr == ')':
                depth -= 1

                end = pos
                if ( depth == 0 ):
                    print(pre, "/from:{}\t to:{}\t s:{}\t -> {}".format(start,end,s,s[start:end]))
                    # return FindBracket(s[start:end] )
                    return s[start:end]


def FindExpr(s, start = 0 , end = 0, depth = 0):
    expressions = ['+','-','*',':','|','&','(',')']
    pos = 0
    for expr in s:
        left  = s[:pos]
        right = s[pos+1:]
        opr   = s[pos:pos+1]

        if right[:1] == "(":
            left = FindBracket(right)
            if FindBracket(left) is not None:
                opr = right[len(left)+2]
                right = right[len(left)+3:]
            
            print("( opr: {}".format(opr))
            print("( lft: {}".format(left))
            print("( rgt: {}".format(right))
            

        if expr in expressions:
            
            
            RIsVar      = isVar(right)
            RIsConst    = isConst(right)
            RIsExpr     = isExpr(right)

            LIsVar      = isVar(left)
            LIsConst    = isConst(left)
            LIsExpr     = isExpr(left)



            print("%")
            print(" Opr:{}\t".format(opr))
            print(" lft:{}\n\tv:{}\tc:{}\te:{}\n".format(left,isVar(left),isConst(left),isExpr(left)))
            print(" rgt:{}\n\tv:{}\tc:{}\te:{}\n".format(right,isVar(right),isConst(right),isExpr(right)))
            

            Raction = ""
            if RIsVar:
                # Raction = Var(right)
                Raction = "Var({})".format(right)
            elif RIsConst:
                # Const(right)
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

        # elif expr in brackets:
           
            # return FindExpr(FindBracket(s[pos:]))
           

        pos += 1


env = { "a" : 2, "b" : 4, "c" : 5, "d" : 3}
for s in rules:
    # print("s:'{}'\t\t -> {}".format(s,FindBracket(s)))
    print("s:'{}'\t\t -> {}".format(s,FindExpr(s)) )
    # print(parts)
    print("---")



# calculator example:
env = { "x" : 3, "y" : 4, "z" : 2}
e1 = Times(Var("z"), Add(Var("y"),Var("x")) )
print(e1.eval(env)) 