#   Did you generate by hand hundreds of dates
#   of working days, from requirement register (quarterly/annually/monthly)
#   and accounting weekends, holidays ???

#   THEN BELOW IS FOR YOU !

'''
  _____                  _      _  _   
 |  __ \                (_)    | || |  
 | |  | | ___  ___ _ __  _ _ __| || |_ 
 | |  | |/ _ \/ _ \ '_ \| | '_ \__   _|
 | |__| |  __/  __/ |_) | | | | | | |  
 |_____/ \___|\___| .__/|_|_| |_| |_|  @hotmail.co.uk
                  | |                  
                  |_|                  
 for bugs/queries.                                           
'''
#   This original script is designed, developed and tested 
#   by Deepin, 2022.
#   for free use only.

# How to use
'''
Edit the three csv files, in same folder as script, to suit your needs. 
- One takes all non working days or holidays, 
that you want output to reflect. //nonworkingdays.csv
- Second takes the start year and finish year. //yearlimits.csv
- Third takes the requirements (quarterly, annually, monthly). //shortlist.csv

When script is run, 
- it reads above three files to take inputs,
- performs date calculations, and
- generates very long list of output as a file.
Its name will be resultlonglist.csv

'''
import calendar as cdr
import pandas as pd
from datetime import datetime as dme

def gtn(lt):
    lt = lt.lower()
    glt = {'q':3, 'h':6, 'a':12}
    return glt[lt[0]] if lt[0] in glt.keys() else 1
def usk(tda):
    y,m,d = [str(a) for a in tda.split('-')]
    return str(d)+'/'+str(m)+'/'+str(y)
def wdf(wdi):
    wvalue = int(str(wdi).lower().replace('wd', ''))
    return wvalue-1 if wvalue>0 else wvalue
fra, frc, yra = pd.read_csv('nonworkingdays.csv', encoding= 'unicode_escape'), pd.read_csv('shortlist.csv').dropna(), pd.read_csv('yearlimits.csv')

yl, yu = yra.loc[0, :].astype(int)[:2]
nwd, nwdt = list(fra['nonworkingdays'].values), []
for h in nwd:
    dobj = dme.strptime(h, '%d/%m/%Y').date()
    nwdt.append(dobj)
cob = cdr.Calendar() 
wdy, dbg = [], {}
for year in range(yl, 1+yu):
    ybg = {}
    for month in range(1, 13):
        mbg = []
        dates = cob.itermonthdates(year, month)
        for i in dates:
            if i not in nwdt and i.weekday() not in [5,6] and i.month==month:
                mbg.append(i)
        ybg[month]=mbg
    dbg[year]=ybg
aev = []  
for _,row in frc.iterrows():
    wd, msd, gp, rps, ev = wdf(row['wd']), row['notbefore'], \
    gtn(row['frequency']), int(row['manyrepeats']), row['event']
    cutoff = dme.strptime(msd, '%d/%m/%Y').date()
    datereminders = [dbg[y][m][wd] for y in dbg for m in dbg[y]]
    trw = [(str(d), str(ev)) for d in datereminders if d>cutoff][::gp][:rps]
    aev = aev + trw
pd.DataFrame([(usk(d), e) for d,e in aev]).to_csv('resultlonglist.csv', index=False, header=False)
# end. 
