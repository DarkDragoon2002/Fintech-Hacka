import http.client
import pandas as pd
import numpy as np

conn = http.client.HTTPSConnection("crypto-news16.p.rapidapi.com")

# Uncomment headers to work. Reason we are not calling is due to limited api calls (Only 5 free so if testing, please only use 1 API call)
headers = {
    # 'X-RapidAPI-Key': "452b9b97efmsh12c07b74b6d831ep17c443jsnc6d448bca78c",
    # 'X-RapidAPI-Host': "crypto-news16.p.rapidapi.com"
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
df = df.drop(["title", "description", "url"], axis=1)
df.to_csv("LatestNews.csv")