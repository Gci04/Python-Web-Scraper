from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.request import urlopen
import numpy as np

site = "https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Russia_by_population"
page = urlopen(site)
soup = BeautifulSoup(page, "html5lib")

population_table=soup.find('table', class_='wikitable sortable')
soup.prettify()
A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
G=[]
H=[]

for row in population_table.findAll("tr"):
    cells = row.findAll('td')
    states=row.findAll('th')
    if len(cells)==7:
        A.append(cells[0].find(text=True))
        B.append(states[0].find(text=True))
        C.append(cells[1].find(text=True))
        D.append(cells[2].find(text=True))
        E.append(cells[3].find(text=True))
        F.append(cells[4].find(text=True))
        G.append(cells[5].find(text=True))
        H.append(cells[6].find(text=True))

for i in range(len(F)):
    F[i] = F[i].replace(",","")
    G[i] = G[i].replace(",","")
    B[i] = B[i].replace(",","")

table_header = ['Rank (2017)','City/Town','Russian','Federal District','Population (2017)','Population (2010)']
data = pd.DataFrame(np.column_stack([B,A,C,E,F,G]),columns=table_header)
data["Population (2010)"] = data["Population (2010)"].astype('int64')
data["Population (2017)"] = data["Population (2017)"].astype('int64')
data["Rank (2017)"] = data["Rank (2017)"].astype('int64')


population_change = ((data["Population (2017)"] - data["Population (2010)"]) /data["Population (2010)"])*100
data["Change%"] = population_change

data.to_csv("population_russia.csv",index=False)
print(data.head(10))
print (data.info())