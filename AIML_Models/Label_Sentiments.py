import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import yfinance as yf

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model = AutoModelForSequenceClassification.from_pretrained("CryptoFinBertFinal")
tokenizer = AutoTokenizer.from_pretrained("Tokenizer")


def predict_label(text, model, tokenizer):
    inputs = tokenizer(text, truncation=True, padding="max_length", max_length=128, return_tensors="pt")
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    single_output = torch.argmax(predictions)
    return single_output.item()

def label_news(csvFilepath):
    df = pd.read_csv(csvFilepath)
    df["label"] = df["text"].apply(lambda x: predict_label(x, model, tokenizer))
    return df

def labels_by_date(df):
    def weight_average(positive, negative, neutral):
        count = positive + negative + neutral
        if count == 0:
            return 0
        else:
            return (positive - negative) / count
    pivot_df = df.pivot_table(index="date", columns="label", aggfunc="size", fill_value=0).reset_index()
    pivot_df.columns = ["Date", "Positive", "Negative", "Neutral"]
    pivot_df["Date"] = pd.to_datetime(pivot_df["Date"])
    pivot_df["Sentiment"] = pivot_df.apply(lambda x: weight_average(x["Positive"], x["Negative"], x["Neutral"]), axis=1)
    return pivot_df

inputFileName = "LatestNews.csv"

df = labels_by_date(label_news(inputFileName))

# Pull Price Data from YFinance
startdate = df['Date'].min()
enddate = df['Date'].max()
data = yf.download("ETH-USD", start=startdate, end=enddate)
df = data.merge(df, how="left", on="Date")
print(df.head())

LSTMDatasetFilepath = 'lstm_data.csv'
df2 = pd.read_csv(LSTMDatasetFilepath)
print(df2.head())
# today = datetime.now()
# outputFileName = ("LSTMOutput" + str(today)).replace(" ", "").replace(":", "-").replace(".", "") + ".csv"
# df.to_csv(outputFileName)