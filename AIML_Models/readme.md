1. CryptoFinBertFinal is the trained Sentiment Analysis Model's weights
2. Tokenizer is the trained Tokenizer for Sentiment Analysis
3. CryptoNewsDataset is the dataset our Sentiment Analysis model was trained on
4. GetNews.py is a API call to https://rapidapi.com/NovusAPI/api/crypto-news16. We use it to get the latest crypto related news. It converts the latest news into a CSV file, LatestNews.csv
    - The reason we don't import it as a module and use the API call directly is due to budget limitations. We are limited to 10 free API calls per month and hence want to reduce the amount of times we call the API for testing purposes. For deployment, given adequate budget, we would subscribe for more API calls.
5. Label_Sentiments does the following:
    - Takes in LatestNews.csv
    - Performs Sentiment Analysis on the latest news
    - Performs data processing
    - Adds it to the lstm_data.csv file in a correct format which can easily be used to train the LSTM.
6. finetuning_finbert_model.py is the python script we used to finetune the sentiment analysis model

HOW TO USE:
    - Run GetNews.py, which will generate a CSV file "LatestNews" with columns date and text
    - Run Label_Sentiments.py, which will update the lstm_data.csv file with the sentiments for today
    - lstm_data.csv can be passed into multivariateLSTM_withSentiment for prediction of actual price
    