import http.client
import pandas as pd
import numpy as np

conn = http.client.HTTPSConnection("crypto-news16.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "452b9b97efmsh12c07b74b6d831ep17c443jsnc6d448bca78c",
    'X-RapidAPI-Host': "crypto-news16.p.rapidapi.com"
}

conn.request("GET", "/news/all", headers=headers)

res = conn.getresponse()
data = res.read()

data = eval(data.decode("utf-8"))
articles = []
for website in data.values():
    articles += website

df = pd.DataFrame.from_records(articles)
df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.date
df['text'] = df['title'] + df['description']
df.drop(["title", "description", "url"], axis=1)
print(df.head())
df.to_csv("LatestNews.csv")