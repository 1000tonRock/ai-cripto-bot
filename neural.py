import numpy as np
import random as r
import pandas as pd
from champs import Vitoriosos 
from bot import tecnicals, getdata
from parabot import tec, TRADE_SYMBOL
from beep import upbeep

dfia = pd.DataFrame()
dfout = pd.DataFrame()
df = pd.DataFrame()
exmult = False

def getdfout():
    u = []
    for i in range(100):
        u.append(False)
    dfout.insert(0,'ignore',u)

    return dfout


def getdfia(x=0):
    data=[]
    ran = 0
    st = '012345678'


    for j in range(0,167):
        data = []
        for i in range(0,100):

            ran = r.uniform(-10,10)
            data.append(ran)
        if x == 0 and (j%4 == 0):
            dfia.insert(j,str(j),Vitoriosos[110])
            continue

        dfia.insert(j,str(j),data)

def getrdata():
    s = r.randint(350,20000)
    x = getdata(TRADE_SYMBOL,'1m',str(s))
    try:
        x = x[:-(s-350)]
    except:
        x = getrdata()

    return x

def block(x=0):
    c =[]
    r=[]
    d=[]
    p = []
    lu = []
    df = getrdata()
    dt = pd.DataFrame()
    tecnicals(df)
    tec(df)


    for i in range(0 , len(df.index)):

        
        a = (df.Close.iloc[i])
        c.append(a)

        b = (df.rsi.iloc[i])/100
        r.append(b)

        e = (df.D.iloc[i])/100
        d.append(e)

        lu.append(0)

        df.ema0.iloc[i] =float(df.ema0.iloc[i])/float(df.Close.iloc[i]) -1
        df.ema1.iloc[i] =float(df.ema1.iloc[i])/float(df.Close.iloc[i]) -1
        df.ema2.iloc[i] =float(df.ema2.iloc[i])/float(df.Close.iloc[i]) -1
        df.ema3.iloc[i] =float(df.ema3.iloc[i])/float(df.Close.iloc[i]) -1
        df.sma0.iloc[i] =float(df.sma0.iloc[i])/float(df.Close.iloc[i]) -1
        df.sma1.iloc[i] =float(df.sma1.iloc[i])/float(df.Close.iloc[i]) -1
        df.sma2.iloc[i] =float(df.sma2.iloc[i])/float(df.Close.iloc[i]) -1

        df.bollh.iloc[i] =float(df.bollh.iloc[i])/float(df.Close.iloc[i]) -1
        df.bolll.iloc[i] =float(df.bolll.iloc[i])/float(df.Close.iloc[i]) -1
        df.bollm.iloc[i] =float(df.bollm.iloc[i])/float(df.Close.iloc[i]) -1

        p_down = df.psar_down.iloc[i] > 0
        p_up = df.psar_up.iloc[i] > 0
           
        if p_up:
            p.append(1)
        else:
            p.append(0)
    

    dt['rsi'] = r
    dt['D'] = d
    dt['psar'] = p
    dt['ema0'] = list(df['ema0'])
    dt['ema1'] = list(df['ema1'])
    dt['ema2'] = list(df['ema2'])
    dt['ema3'] = list(df['ema3'])
    dt['sma0'] = list(df['sma0'])
    dt['sma1'] = list(df['sma1'])
    dt['sma2'] = list(df['sma2'])
    dt['bollh'] = list(df['bollh'])
    dt['bolll'] = list(df['bolll'])
    dt['bollm'] = list(df['bollm'])
    dt['macd'] =list(df['macd'])
    dt['gab'] = c
    return dt



def ia(im1,num,r=0):
    global dfia
    if r == 0:
        l = list(dfia.loc[num])
    else:
        l = num

    neu1 = []
    neu2 = []

    ls = []
    ls.append(l[:15])
    ls.append(l[15:30])
    ls.append(l[30:45])
    ls.append(l[45:60])
    ls.append(l[60:75])
    ls.append(l[75:90])
    ls.append(l[90:105])
    ls.append(l[105:120])

    ls.append(l[120:128])
    ls.append(l[128:136])
    ls.append(l[136:144])
    ls.append(l[144:152])
    ls.append(l[152:160])

    ls.append(l[160:165])


    bias = l[-2]
    lim = l[-1]
    out = 0

    for i in range(8):
        o = sum(np.multiply(im1,ls[i]))
        neu1.append(o)
        
    
    for i in range(8,13):
        o = sum(np.multiply(neu1,ls[i]))
        neu2.append(o)
        
    
    out = sum(np.multiply(neu2,ls[-1])) + bias
 
    
    out = np.tanh(out)
    lim = np.tanh(lim)
    
    if out > lim:
        output = True
    else:
        output = False
    
    return output
    
def strategy(l=0,r=0):
    global df , dfout
    p = []

    for j in range(1,len(df.index)):
        outs = []
        
        
    
        for i in range(100):
            cont = 0
            
            im1 = list(df.loc[j])
            im1 = im1[:-1]


            if r == 0:
                p = list(dfout.loc[i])
                auxp = p
                n = i
            else:
                if i !=0:
                    break

                auxp = p
                n = l
                if j == 1:
                    auxp = [False]
                    p = []

                n = l
                

            v = auxp[-1]
            
            
            if not v:
                for k in p[::-1]:
                    if k:
                        auxp = p[-cont :]
                    cont = cont + 1
            if v:
                for k in p[::-1]:
                    if not k:
                        auxp = p[-cont :]
                    cont = cont + 1
            
            

            perf = calc(calculation(auxp,1))
            im1.append(perf)
            im1 = delnone(im1)
            outs.append(ia(im1,n,r))

            if r != 0:
                p.append(outs[-1])
        
        
        if r == 0:
            dfout.insert(j,str(j),outs)
        
    if r != 0:
        y = []
        x = calc(calculation(p,1)) 
        
        y.append(x)
        
        y = delnone(y)
       
        x = y[-1]

        x = x*100
        return x



def calculation(c,z=0,dfy=df):
    global df,dfout
    aux = []
    cal =[]

    
    if z == 0:
        mem = list(dfout.loc[c])
        mem = mem[1:]
    else:
        mem = c
    
    g = list(dfy['gab'])
    gab = g
    b = False
    cont = 0
    for i in mem:
        if b and (not i):
            aux.append(cont) 
            b = False
            cont = cont + 1
            continue
            
        if i and (not b):
            aux.append(cont)
            b = True
            cont = cont + 1
            continue

        
        cont = cont + 1
        
    for i in aux:
       cal.append(gab[i])
    
    
    return cal
    
def calc(closes):
    jump = 1
    L = []
    for c in range(1,len(closes)):
        if c == jump:
            continue

        try:
            lucro = (closes[c])/(closes[c - 1]) - 1
            
            L.append(lucro)

            jump = c+1

        except Exception as e:
            print("fim do array - {}".format(e))

        total = 1
        for l in range(len(L)):
            total = total + (total * L[l])

        total = total - 1


        return total



def reward():
    rew = []
    for i in range(len(dfia.index)) :
       rew.append(calc(calculation(i)))
    return rew

def selection(rew):
    global exmult
    sel = [[0,0,0,0],[0,0,0,0]]

    for i in range(4):
        f = max(rew)
        print(f)
        sel[0][i] = rew.index(f)
        sel[1][i] = (f)*100
        rew[rew.index(f)] = -10

    return sel

def mutation(wn,s):
    global exmult
    w = [0,0,0,0]

    for i in range(len(wn)):
        w[i] = list(dfia.loc[wn[i]])
        
    if s == w[0]:
        pass
    else:
        w[-1] = s

    dat = []
    for i in range(0,167):

        ra = r.uniform(-10,10)
        dat.append(ra)
        
    p0 = True
    p1 = False
    p2 = False
    p3 = False
    p4 = False
    
    for i in range(len(dfia.index)):
        if p0:
            dfia.loc[i] = w[0]
            p1 = True
            p0 = False
            
        if p1:
            dfia.loc[i] = w[1]
            p2 = True
            p1 = False
        if p2:
            dfia.loc[i] = w[2]
            p3 = True
            p2 = False
        if p3:
            dfia.loc[i] = w[3]
            p4 = True
            p3 = False
        if p4:
            dfia.loc[i] = dat
            p0 = True
            p4 = False

    aux =[]
    
    x = 0
    for i in range(len(dfia.index)):

        aux = list(dfia.loc[i])
        nmut = 55
        used =[]
        while x < nmut:
            loc1 = r.randint(0,166)

            if loc1 in used:
                loc1 = r.randint(0,166)
            
            
            if not exmult:
                aux[loc1] =  r.uniform(-10,10)
            if exmult:
                aux[loc1] = aux[loc1] * r.uniform(-2,2)
            used.append(loc1)
            x = x + 1
        
        dfia.loc[i] = aux
        if i == 89:
            dfia.loc[i] = s 
    return w

def delnone(mylist):
    mylist = [str(x) for x in mylist]
    for i in range(len(mylist)):
        if mylist[i] == 'None':
            mylist[i] = 0
    
    mylist = [float(x) for x in mylist ]
    return mylist

def progress(v):
    vv = []
    for i in v:
        c = strategy(i,1)
        
        vv.append(c)
    
    vvv = [max(vv), vv.index(max(vv))]
    return vvv


def main():
    numg = int(input("Numero de Geracoes:"))
    gn = 0

    global df, dfia, dfout

    getdfia(1)
    print(dfia)
    gen = []
    vitoriosos =[]
    ppp =[]
    

    while gn < numg:
        
        
    
        gn = len(gen) + 1
        print('Geracao:{}'.format(gn))

        
        print('Criando Bloco . . .')

        df = block()

        print(df)

        c = 0
        fail = True
        while fail:
            if c == 0:
                fail = False
                c = c+1
            dfout = pd.DataFrame()
            dfout = getdfout()

            print('Treinando . . .')
            
            strategy()
            
            print(dfout)
            
            print('Calculando os melhores . . .')

            rew = reward()
            rew = delnone(rew)
            print(rew)

            # index das quatro melhores / lucro
            win = selection(rew)

            # index das quatro melhores
            t = win[0]
            print('t:{}'.format(t))

            # index da melhor IA
            tbest = win[0][0]
            print('tbest:{}'.format(tbest))

            vitoriosos.append(list(dfia.loc[tbest]))     
            pp = progress(vitoriosos)
            ppp.append(pp)
            mdgen = ppp[-1]
            
            if not fail:
                cont = 0
            if (mdgen[0] <= win[1][0]) and (tbest != 89):    
                fail = False
                cont = 0
            else:
                fail = True
                vitoriosos = vitoriosos[:-1]
                ppp = ppp[:-1]
                log = open('champs.txt', 'a')
                log.write("Fail: ")
                log.close()
                if cont >= 25:
                    fail = False
                cont = cont + 1
            
            sub = vitoriosos[pp[1]]
            print(mdgen,gn-1)
            
            print('Mutando . . .')
            w = mutation(t,sub)

               
        print(w)
        gen.append(win)
        print(win)
        log = open('champs.txt', 'a')
        log.write("0{}: ".format(gn - 1))
        log.write("{}\n".format(win))
        log.write("Melhor de cada: {}\n\n".format(mdgen))
        log.close()

    log = open('champs.txt', 'a')
    log.write("Vitoriosos: {}\n".format(vitoriosos))
    log.write("Melhor de cada: {}\n\n".format(ppp))
    log.close()



    upbeep()

    

        


if __name__ == '__main__':
    main()
