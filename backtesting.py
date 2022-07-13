from ia import *
from lucroCalc import calc
import winsound
import os
from champs3 import Vitoriosos
from neural import ia, strategy, calc, calculation, delnone

#win = Vitoriosos[-1]

time_inicial = time.time()
grup = '10300'
# df = dfr('dydxbusd080522.txt')
df = blockx(grup)
#df = df[:-480]
#tecnicals(df)

log = open(doc, 'a')
log.write("{}\n".format(TRADE_SYMBOL))
log.close()

p = []

for i in range(2 , len(df.index)):
    new_df = df[:i]

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
    
    out = strat(win,new_df,auxp)

    p.append(out)

print(df)

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)
print('Demorou: {}'.format(time.time() - time_inicial))

