from os import get_inheritable
import re



ruleLine = "long+(short+extended_a)"
# rules = ["1*(2+(4+8)+9)*10"]
rules = ["a*(b+(c+d)+e)*f"]


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
    if not isinstance(field,str):
        return False
    if re.search("[\+\-\*\:\|\&\!\^]", field) :
        return True
    return False

def isVar(field) :
    # if isinstance(field,Expr):
    #     return False
    if re.search("^[a-zA-Z]", field) and not isExpr(field) : 
        return True
    return False

def isConst(field):
    # if isinstance(field,Expr):
    #     return False
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
                # print(pre, "\str:{}\t s:{}".format(start,s[start:]))
                # result = FindBracket(s,pos = pos+1, open = open, start = start)
                # print (pre, "result:" + result + " " + str(start) )
                # return result
            elif expr == ')':
                depth -= 1

                end = pos
                if ( depth == 0 ):
                    # print(pre, "/from:{}\t to:{}\t s:{}\t -> {}".format(start,end,s,s[start:end]))
                    # return FindBracket(s[start:end] )
                    return s[start:end]

def Qualify(Input):
    if Input == 'd':
        print ("Special D")
    if isinstance(Input,Expr):
        return Input
    if isVar(Input):
        strResult = "Var({})".format(Input)
        Result = Var(Input)
    elif isConst(Input):
        strResult = "Const({})".format(Input)
        Result = Const(Input)
    else:
        strResult = Input
        Result = Input
    # return strResult
    return Result

def Operator(Operation, LAction, RAction):
    if Operation == "*":
        straction = "Times({},{})".format(LAction,RAction)
        action = Times(LAction,RAction)
    elif Operation == "+":
        straction = "Add({},{})".format(LAction,RAction)
        action = Add(LAction,RAction)
    # return straction
    return action

def FindExpr(s, start = 0 , end = 0, depth = 0):
    expressions = ['+','-','*',':','|','&']
    pos = 0
    for expr in s:
        left  = s[:pos]
        right = s[pos+1:]
        opr   = s[pos:pos+1]

        # RIsVar      = isVar(right)
        # RIsConst    = isConst(right)
        # RIsExpr     = isExpr(right)

        # LIsVar      = isVar(left)
        # LIsConst    = isConst(left)
        # LIsExpr     = isExpr(left)

        if right[:1] == "(":
            SubExpr = FindBracket(right)
            SubExprLen = len(SubExpr)
            rightLen = len(right)
            # if 
            if SubExprLen < rightLen:
                llen = SubExprLen + 3
                rlen = (rightLen - (llen))*-1
                # print ("L_leftpart: {} \t{}\t {} right part".format(SubExpr,opr,right[llen:]))
                # Find The operation
                opr = right[SubExprLen+2]
                
                wrkRight = Qualify(FindExpr(SubExpr))
                wrkLeft = Qualify(right[rlen:])
                # Store operation
                right = Qualify(Operator(opr,wrkLeft, wrkRight ))
                print("Type: ", str(type(right)))
                # Within braces Qualify Right as Expression
                # RIsVar = isVar(right)
                # RIsConst = isConst(right)
                # RIsExpr = isExpr(right)

        if left[:1] == "(":
            SubExpr = FindBracket(left)
            SubExprLen = len(SubExpr)
            leftLen = len(left)
            if SubExprLen < rightLen:
                llen = SubExprLen + 3
                rlen = (rightLen - (llen))*-1
                print ("R_leftpart: {} \t {} right part".format(SubExpr,left[llen:]))
                left = FindExpr(SubExpr)
                opr = left[SubExprLen+2]
                # right = left[rlen:]

        
        if expr in expressions:
            print("( opr: {}".format(opr))
            print("( lft: {}".format(left))
            print("( rgt: {}".format(right))

            if right is 'd':
                print("special:{}\n\tv:{}\tc:{}\te:{}\n".format(right,isVar(right),isConst(right),isExpr(right)))



            # print("%")
            # print(" Opr:{}\t".format(opr))
            # print(" lft:{}\n\tv:{}\tc:{}\te:{}\n".format(left,isVar(left),isConst(left),isExpr(left)))
            # print(" rgt:{}\n\tv:{}\tc:{}\te:{}\n".format(right,isVar(right),isConst(right),isExpr(right)))
            
            # Raction = ""
            # if RIsVar:
            #     Raction = Var(right)
            #     # Raction = "Var({})".format(right)
            # elif RIsConst:
            #     Raction = Const(right)
            #     # Raction = "Const({})".format(right)
            # elif RIsExpr:
            #     # Raction = FindExpr(right)
                # if right[:1] == '(':
                #     SubExpr = FindBracket(right)
                #     if len(SubExpr) < len(right):
                #         print ("leftpart: {} \t {} right part".format(SubExpr,right[len(SubExpr)+2:]))
                # right = FindExpr(right)
                # Raction = "{}".format(right)
                # Raction = Qualify(right)

            # Laction = ""
            # if LIsVar:
            #     Laction = Var(left)
            #     # Laction = "Var({})".format(left)
            # elif LIsConst:
            #     Laction = Const(left)
            #     # Laction = "Const({})".format(left)
            # elif LIsExpr:
            #     # Laction = FindExpr(left)
            #     # left = FindExpr(left)
            #     # Laction = "{}".format(left)
            #     Laction = Qualify(left)
                # start nesting from here. 
            

            action = Operator(opr,Qualify(left),Qualify(right))
           
            return action
        pos += 1


env = { "a" : 1, "b" : 2, "c" : 4, "d" : 8, "e" : 9, "f":10}
for s in rules:
    # print("s:'{}'\t\t -> {}".format(s,FindBracket(s)))
    print("s:'{}'\t\t -> {}".format(s,FindExpr(s).eval(env)) )
    # print(parts)
    print("---")



# calculator example:
env = { "x" : 3, "y" : 4, "z" : 2}
e1 = Times(Var("z"), Add(Var("y"),Var("x")) )
print(e1.eval(env)) 