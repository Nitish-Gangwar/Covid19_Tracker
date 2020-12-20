import requests
import json
from bs4 import BeautifulSoup
url="https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/"

r=requests.get(url)
soup=BeautifulSoup(r.content,'html.parser')
states=[]
state_name=""
d={}
state_arr=[]
district_arr=[]
for i in soup.find_all("div","skgm-states"):
    state=[]
    for j in i.find_all("span","show-district"):
        #got the state name
        state.append(j.text)
        state_name=j.text
        state_name=state_name.replace(' ','_')

    districts=[]
    dis=[]
    for res in i.find_all('div'):
        count=0

        for k in res.find_all("div","skgm-tr"):
            count=0
            district=[]
            for l in k.find_all("div","skgm-td"):
                if(count==0):
                    district.append(l.text)
                    dis.append(l.text)
                count+=1
    d[state_name]=dis
    print("state_name= ",state_name,d[state_name])
geeky_file = open('geekyfile.txt', 'wt') 
geeky_file.write(str(d)) 
geeky_file.close() 

    
