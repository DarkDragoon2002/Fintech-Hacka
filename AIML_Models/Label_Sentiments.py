import pandas as pd
import numpy as np
from pathlib import Path

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
    print(predictions)
    return single_output.item()

print(predict_label("US interest rate to remain high", model, tokenizer))
print(model.config.id2label)

df = pd.read_csv("CryptoNewsDataset.csv")
df["text"] = df["title"] + df["text"]
df = df.drop(["sentiment", "title", "source", "subject"], axis=1)
df["date"] = pd.to_datetime(df["date"], yearfirst=True)
df["date"] = df["date"].dt.date
df["label"] = df["text"].apply(lambda x: predict_label(x, model, tokenizer))

df.to_csv(filepath)