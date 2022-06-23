import numpy as np
import pandas as pd
from bot import tecnicals, getdata, order
from parabot import tec, TRADE_SYMBOL, TRADE_QUANTITY
from datetime import datetime
import time
import config
from binance.client import Client
from binance.enums import *
from neural import ia, calc, calculation, delnone

win = [8.324759,-1.898609,-14.911500,-16.973872,37.006412,-11.993565,-4.140622,1.079467]
in_position = False
doc = 'ia.txt'
subtraction = 0
error = False
kill = False

def blockx(y="350"):
    c =[]
    r=[]
    d=[]
    p = []
    lu = []
    df = getdata(TRADE_SYMBOL,'1m',y)
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
    dt['Time'] = df.index
    dt['gab'] = c

    return dt

def strat(win,dfy,auxp):
    global in_position,subtraction, error, kill,doc

    im1 = list(dfy.loc[len(dfy.index) -1 ])
    im1 = im1[:-2]
    perf = calc(calculation(auxp,1,dfy))
    im1.append(perf)
    im1 = delnone(im1)

    
    out = ia(im1,win,1)

    
    close_now = float(dfy.gab.iloc[-1])
    # macd_now = float(df.macd.iloc[-1])
    time_now = dfy.Time.iloc[-1]

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
            #order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
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
            print("sell")
            if not error:
                k = TRADE_QUANTITY

            # put binance sell logic here
            #order_succeeded = order(SIDE_SELL, k, TRADE_SYMBOL)
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
                k = k - subtraction
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
        
        df = block()

        auxp = p

        v = auxp[-1]
        
        if not v:
            auxp = []
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
