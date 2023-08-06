#ASMDR operations

def add(*args):
    return sum(list(args))

def sub(*args):
    List=list(args)
    a=List[0]
    List.remove(List[0])
    for i in List:
        a=a-i
    return a


def mul(*args):
    List=list(args)
    a=List[0]
    List.remove(List[0])
    for i in List:
        a=a*i
    return a

def div(a,b):
    return a/b

def rem(a,b):
    return a%b    

#power operations 
def s2(a):
    return a**2
    
def pow(a,b):
    return a**b

def sq_rt(a):
    return a**(1/2) 

#step function/gif
from math import *

def gif(a):
    return floor(a)

