import pandas as pd
import winsound
import math
duration = 1000  # milliseconds
freq = 440  # Hz
data = pd.DataFrame()

df_chunk = pd.read_csv('./data/SequentialPatterns.csv', dtype = str, usecols = ['Pattern'] , squeeze = True) #, chunksize = 1000
setp = set()
for c in df_chunk:
    d = c.split(';')
    #print(d)
    for e in d:
        f = e.split('_')
        setp.add(f[0])
        #print(f[0])
        # input('w')
for p in setp:
    print(p)

winsound.Beep(freq, duration)
'''

chunk_list = []  

for i, chunk in enumerate(df_chunk):  
    if i%100 == 0:
        chunk_list.append(chunk)
data = pd.concat(chunk_list, ignore_index= True)
data.reset_index(drop = True)

data.to_csv('./data/AllEvents_EntireData.csv', index = False)

zips = set()
for chunk in data:
    for i in range(len(chunk)):
        if len(chunk.iloc[i]):
            print(chunk.iloc[i])
            input('w')
        zips.add(chunk.iloc[i])
        
print(zips)

'''
