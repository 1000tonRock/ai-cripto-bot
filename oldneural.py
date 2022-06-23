import numpy as np
import pandas as pd
from bot import tecnicals, getdata
from parabot import tec, TRADE_SYMBOL

def block():
    df = getdata(TRADE_SYMBOL,'1m','300')
    tec(df)
    tecnicals(df)
    return df


def ia(im1,num):
    l = df1.loc[num]
    la = l(,7)
    bias = l[-2]
    lim = l[-1]
    out = 0
    
    out = sum(np.multiply(im1,la)) + bias
 
    
    out = np.tanh(out)
    
    if out > lim:
        output = True
    else:
        output = False
    
    return output
    
def strategy():
    im1 = df.loc[-1]


    for i in range(,100):
       outs.append(ia(im1,i))
    
    df2.insert(outs)

def calculation(c):
    aux = []
    mem = df2.loc(c)
    gab = df['Closes']
   
    for i in mem:
        if b and (not i):
            aux.append(mem.index(i)) 
            b = False
            
        if i and (not b):
            aux.append(mem.index(i))
            b = True
        
    for i in aux:
       i = gab[i]
    
    return aux
    
calc()

def reward():
    rew = []
    for i in df.index :
       rew.append(calc(calculation(i)))
    return rew

def selection(rew):
    f = max(rew)
    f = rew.index(f)
    rew.remove(f)
    s = max(rew)
    s = rew.index(s)
    rew.remove(s)
    t = max(rew)
    t = rew.index(t)
    rew.remove(t)
    q = max(rew)
    q = rew.index(q)
    rew.remove(q)
    k = max(rew)
    k = rew.index(k)
