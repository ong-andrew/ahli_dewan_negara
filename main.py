import csv, requests, pickle, time
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd

with open('urls.pkl', 'rb') as f:
    urls = pickle.load(f)
    
new_list = []

i = 0

while True:
    if i == len(urls):
        break
    
    headers = {'user-agent': 'my-agent/1.0.1'}
    site = requests.get(urls[i], headers=headers).text
    soup = BeautifulSoup(site,'lxml')
    table = soup.find("td")
    lines = table.find_all("tr")

    dict1 = {}
    
    for line in lines:
        if line.find("strong"):
            dict1[line.find_next().get_text()] = line.find_next().find_next().find_next().get_text().replace("\r","").replace("\n","")
    
    new_list.append(dict1)
    i += 1
    print(dict1)
    time.sleep(2)
    
df = pd.DataFrame(new_list)
df = df[["Nama","Parti","Lantikan","Tempoh","Lantikan Semula","Negeri","Jawatan dalam Parlimen",'No. Telefon', 'No. Faks', 'Email', 'Alamat Surat-menyurat',"Media Sosial"]]
df.rename(columns = {'Lantikan Semula':'Lantikan_Semula'}, inplace = True)
df["Expiry"] = df["Lantikan_Semula"]
df['Expiry'] = df['Expiry'].fillna(df.Tempoh)
df['Expiry2'] = df['Expiry'].str.split(' ').str[-1]
df = df[["Nama","Parti","Expiry2","Tempoh","Lantikan_Semula","Negeri","Jawatan dalam Parlimen",'No. Telefon', 'No. Faks', 'Email', 'Alamat Surat-menyurat',"Media Sosial","Lantikan","Expiry"]]
df["Expiry2"] = pd.to_datetime(df["Expiry2"]).dt.date
df.head(2)
df.to_csv("test.csv", index=False)
