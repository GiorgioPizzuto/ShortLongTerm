import pandas as pd 

fileread = pd.read_csv('./data/frequent_trees_City_MSF-0.05_MTL-25.csv') # , usecols = ['Pattern'], squeeze= True
patterns = set()
for p in fileread['Pattern']:
    patterns.add(p)
patterns = list(patterns)
patterns.sort()
print(len(patterns))

for i, p in enumerate(patterns):
    data_pattern = fileread.loc[fileread['Pattern'] == p]
    city = data_pattern['City']
    setcity = set()
    for c in city:
        setcity.add(c.split('-')[1])
    print(i, len(setcity), round(data_pattern['Support'].mean(), 3), p)


'''
for index, row in data_pattern.iterrows():
     print(index, row)    

for p in patterns:
    print(p)
print(len(patterns))
print(len(fileread))

'''
