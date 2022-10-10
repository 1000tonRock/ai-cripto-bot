import numpy as np
import random as r
import pandas as pd
import time
from champs4 import Vitoriosos 
from bot import tecnicals, getdata
from parabot import tec
from beep import upbeep
#from dfwriter import dfr

time_inicial = time.time()
dfia = pd.DataFrame()
dfout = pd.DataFrame()
df = pd.DataFrame()
exmult = False
olddata = 'dydxbusd080522.txt'
doc = 'champs.txt'

TRADE_SYMBOL = 'ETHUSDT'
TRADE_SYMBOL2 = 'ETHDOWNUSDT' 

Vitoriososz =[]

for i in Vitoriosos[-1]:
    x=i
    x=int(x)
    Vitoriososz.append(x)

def getdfout():
    u = []
    for i in range(100):
        u.append(False)
    dfout.insert(0,'ignore',u)

    return dfout

trei = [-5.179513,-8.271835,4.521662,-1.927740,12.996615,14.206938,-1.846567,0.242029,-4.511521]

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
            dfia.insert(j,str(j),Vitoriosos[-1])
            continue

        dfia.insert(j,str(j),data)

# get random data from binance:
def getrdata():
    print('bloco 1')
    s = r.randint(350,20000)
    x = getdata(TRADE_SYMBOL,'1m',str(s))
    try:
        x = x[:-(s-350)]
    except:
        x = getrdata()

    return x

def getrdata2():
    print('bloco 2')
    s = r.randint(350,20000)
    x = getdata(TRADE_SYMBOL2,'1m',str(s))
    try:
        x = x[:-(s-350)]
    except:
        x = getrdata2()

    return x

# organiza os dados no bloco:
def block(x=0, old=0):
    # remover x # old define se vai recebar dados antigos

    c =[]
    ri=[]
    d=[]
    p = []
    lu = []
    
    if old != 0:
        # df = dfr(olddata)
        return df

      
    # alterar para duas db aleatoria
    rint = r.randint(0,1)

    if rint:
        df= getrdata()
    else:
        df =getrdata2()

    dt = pd.DataFrame()
    tecnicals(df)
    tec(df)


    for i in range(0 , len(df.index)):

        
        a = (df.Close.iloc[i])
        c.append(a)

        b = (df.rsi.iloc[i])/100
        ri.append(b)

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
    

    dt['rsi'] = ri
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

        try:
            o = sum(np.multiply(im1,ls[i]))
        except:
            print('im1: {}'.format(im1))
            print('ls[i]: {}'.format(ls[i]))
            exit()
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

    # for k in range(100,len(df.index)*100):
    for j in range(1,len(df.index)):
        #j = int(k/100) 
        #i = k -j*100

        # if i==0
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
        
        # if i==0:
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


# junta a lista de valores de compra e vendas executados
def calculation(c,z=0,dfn=0):
    global df,dfout
    aux = []
    cal =[]
    try:
        if dfn == 0:
            dfy = df
    except:
        dfy = dfn
        

    
    if z == 0:
        mem = list(dfout.loc[c])
        mem = mem[1:]
    else:
        mem = c

    # caso titulos sejam diferentes
    try:
        g = list(dfy['gab'])
    except:
        g = list(dfy['o'])

    gab = g
    b = False
    cont = 0

    # correção do tamanho do mem
    if len(gab) < len(mem):
        mem = mem[-len(gab)::]
        
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
        try:
            cal.append(gab[i])

        except Exception as e:
            print('ERROR IN CAL - {}'.format(e))

            print('i - {}'.format(i))
            print('aux - {}'.format(aux))
            print('gab - {}'.format(gab))
            print('cal - {}'.format(cal))
    
    
    return cal
    
def calc(closes):
    jump = 1
    L = []
    lost = []
    good = 0
    bad = 0
    perda = 0

    # corrigir numero 1, desordena o calculo dos closes
    for c in range(len(closes)):
        if c == jump:
            continue

        try:
            lucro = (closes[c])/(closes[c - 1]) - 1
            
            if lucro > 0:
                good = good + 1
            else:
                bad = bad + 1
                lost.append(lucro)
                if perda > lucro:
                    perda = lucro

            L.append(lucro)

            jump = c+1

        except Exception as e:
            print("fim do array - {}".format(e))

    # erro: total dentro do for

    total = 1
    for l in range(len(L)):
        total = total + (total * L[l])

    total = total - 1

    # taxa de acerto
    if (bad !=0) or (good != 0):
        winrate = (good/(bad+good))
    else:
        winrate = 0
    
    # multiplica pela taxa de acerto, para ter mais peso o acerto
    return total*winrate



def reward():
    rew = []
    for i in range(len(dfia.index)) :
       rew.append(calc(calculation(i)))
    return rew

def selection(rewx,x=1):
    # alterar a seleção para aceitar 20 
    rew = list(rewx)
    sel = [[0,0,0,0],[0,0,0,0]]

    lastsel = [[],[]]
    for k in range(20):
        lastsel[0].append(0)

    cont = 0
    for i in range(20):

        f = max(rew)
        if cont == 0:
            firstf = f
            cont=cont+1

        # retira zeros e substitui pela melhor
        if (firstf > f) and (f == 0):
            print('zero flag')
            if i < 4 :
                sel[0][i] = sel[0][0]
            lastsel[0][i] = lastsel[0][0]
            continue

        print(f)

        lastsel[0][i] = rew.index(f)

        if i < 4 :
            sel[0][i] = lastsel[0][i]
            sel[1][i] = (f)*100

        

        rew[rew.index(f)] = -10

    if x == 1:
        return sel
    if x == 2:
        return lastsel

def mutation(wn,s):
    global exmult
    w = []
    for i in range(len(wn[0])):
        w.append(0)

    for i in range(len(wn[0])):
        w[i] = list(dfia.loc[wn[0][i]])
        
    

 
    
    ## alterar esse trecho para um range de termos de w
    j=0
    for i in range(len(dfia.index)):
        # print('i = {}'.format(i))
        # print('j = {}'.format(j))
        dfia.loc[i] = w[j]

        j = j + 1
        if j >= 20:
            j=0
     

    aux =[]
    
    x = 0
    for i in range(len(dfia.index)):
        # adicionar um if para nao mutar todos os individuos x=1/33 == 3%
        ind1 = r.randint(0,32)
        if ind1 != 32:
            continue


        aux = list(dfia.loc[i])
        nmut = 5 # numero de genes mutados nmut = 5
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
    ml = list(mylist)
    for i in range(len(ml)):           
        if ml[i] == 'None':
            ml[i] = 0
    ml = [float(x) for x in ml]
    return ml

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

        df = block(0,0)

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
            # index das 20 melhores: 2 -> 20 melhores
            win20 = selection(rew,2)

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
                log = open(doc, 'a')
                log.write("Fail: ")
                log.close()
                if cont >= 25:
                    fail = False
                cont = cont + 1



            try:
                sub = vitoriosos[pp[1]]
            except:
                print ('error in sub')
                print('pp {}'.format(pp))
                print('vitoriosos {}'.format(vitoriosos))
                exit()

            print(mdgen,gn-1)
            
            print('Mutando . . .')
            # para não estagnar na falha

            print(win20)
            
            if fail and (win[1][0] > win[1][1]):
                x = win20[0][0]
                for i in range(len(win20[0])):
                    win20[0][i] = x
            print(win20)

            #mutação
            w = mutation(win20,sub)

               
        #print(w)
        gen.append(win)
        print(win)
        log = open(doc, 'a')
        log.write("0{}: ".format(gn - 1))
        log.write("{}\n".format(win))
        log.write("Melhor de cada: {}\n\n".format(mdgen))
        log.close()

    log = open(doc, 'a')
    log.write("Vitoriosos: {}\n".format(vitoriosos))
    log.write("Melhor de cada: {}\n\n".format(ppp))
    log.close()



    upbeep()

    

        


if __name__ == '__main__':
    main()
    print('Demorou: {}'.format(time.time() - time_inicial))