import numpy as np
import pandas as pd
from bot import tecnicals, getdata, order, client
from parabot import tec
from datetime import datetime
import time
import config
from binance.client import Client
from binance.enums import *
from neural import ia, strategy, calc, calculation, delnone
from champs4 import Vitoriosos

win = Vitoriosos[-1]
TRADE_SYMBOL = 'ETHUSDT'
TRADE_QUANTITY = 10.3 #USD
subtraction = -0.0001
doc = 'ia.txt'
in_position = False
error = False
kill = False

def iax(im1,w):
    global dfia
    l = w
    la = l[:6]
    bias = l[-2]
    lim = l[-1]
    out = 0
    
    out = sum(np.multiply(im1,la)) + bias
 
    
    out = np.tanh(out)
    lim = np.tanh(lim)
    
    if out > lim:
        output = True
    else:
        output = False
    
    return output

def blockx(y="350",t=TRADE_SYMBOL):
    c =[]
    r=[]
    d=[]
    p = []
    lu = []
    df = getdata(t,'1m',y)

    if type(df) == bool:
        print("waiting for connection")
        time.sleep(1)
        return blockx(y)

    dt = pd.DataFrame()
    tecnicals(df)
    tec(df)
    print(df)


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
    # dt['Time'] = df.index
    dt['gab'] = c

    return dt

def strat(win,dfy,auxp):
    global in_position,subtraction, error, kill,doc, TRADE_QUANTITY

    im1 = list(dfy.loc[len(dfy.index) -1 ])
    im1 = im1[:-1]
    perf = calc(calculation(auxp,1,dfy))
    per = delnone([perf])
    perf = per[0]
    im1.append(perf)
    
    out = ia(im1,win,1)

    try:
        close_now = float(dfy.gab.iloc[-1])
        # macd_now = float(df.macd.iloc[-1])
        time_now = str(datetime.now())
        # dfy.Time.iloc[-1]
    except:
        close_now = float(dfy.o.iloc[-1])
        time_now = 42

    print('atual close: {}'.format(close_now))
    # print('atual MACD: {}'.format(macd_now))
    print('atual time: {}'.format(time_now))
    # print()
    # print("buy position = {}".format(in_position))
    # print()


    if out:
        if in_position:
            print("you already have it, nothing to do")
        else:
            print("BUY!BUY!BUY!")
            # put binance buy order logic here
            # order_succeeded = order(SIDE_BUY, (TRADE_QUANTITY/close_now), TRADE_SYMBOL)
            order_succeeded =[True,close_now]

            if order_succeeded[0]:
                buyprice = order_succeeded[1]
                last_buy = buyprice

                log = open(doc, 'a')
                log.write("Buy! Buy! Buy!: {}\n".format(last_buy))
                # log.write("MACD: {}\n".format(macd_now))
                log.write("Time: {}\n".format(time_now))
                
                log.close()
                in_position = True
        return out
    
    if not out:
        if in_position:
            print("Sell! Sell! Sell!")

            # put binance sell logic here
            # order_succeeded = order(SIDE_SELL, (TRADE_QUANTITY/close_now), TRADE_SYMBOL)
            order_succeeded = [True, close_now]

            if order_succeeded[0]:
                sellprice = order_succeeded[1]
                log = open(doc, 'a')
                log.write("Sell! Sell! Sell!: {}\n".format(sellprice))
                # log.write("MACD: {}\n".format(macd_now))
                log.write("Time: {}\n".format(time_now))
                
                log.close()
                in_position = False

                if error:
                    kill = True
            if not order_succeeded[0]:
                error = True
                TRADE_QUANTITY = TRADE_QUANTITY - subtraction
        else:
            print("you don't have any, nothing to do")
        return out

def main():

    
    global doc

    log = open(doc, 'a')
    log.write("{}\n".format(TRADE_SYMBOL))
    log.write("{}\n".format(str(datetime.now())))
    log.write("\n")
    log.close()
    p = []
    auxp = []

    while True:

        if kill:
            exit()
        
        df = blockx()

        auxp = p

        try:
            v = auxp[-1]
        except:
            v = False

        cont = 0
        if (not v) and (len(p) != 0):
            for k in p[::-1]:
                if k:
                    auxp = p[-cont :]
                cont = cont + 1
        if v:
            for k in p[::-1]:
                if not k:
                    auxp = p[-cont :]
                cont = cont + 1
                
        out = strat(win,df,auxp)
        p.append(out)
        time.sleep(60)

if __name__ =='__main__':
    main()