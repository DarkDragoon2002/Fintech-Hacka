import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model = AutoModelForSequenceClassification.from_pretrained("CryptoFinBertFinal")
tokenizer = AutoTokenizer.from_pretrained("Tokenizer")

filepath = Path('Labelled_Dataset.csv')

def predict_label(text, model, tokenizer):
    inputs = tokenizer(text, truncation=True, padding="max_length", max_length=128, return_tensors="pt")
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    single_output = torch.argmax(predictions)
    return single_output.item()

def label_news(csv_filepath):
    df = pd.read_csv(csv_filepath)
    df["label"] = df["text"].apply(lambda x: predict_label(x, model, tokenizer))
    df.to_csv(filepath)
    return df

def output_to_LSTM(df):
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

df = output_to_LSTM(label_news(inputFileName))
print(df.head())
today = datetime.now()
outputFileName = ("LSTMOutput" + str(today)).replace(" ", "").replace(":", "-").replace(".", "") + ".csv"
df.to_csv(outputFileName)