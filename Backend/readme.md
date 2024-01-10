Main Features of API
1. Impermanent Loss Prediction: Utilize the /predict_impermanent_loss endpoint to predict Impermanent Loss based on specified parameters such as Range Percentage, Mean, and Standard Deviation. Impermanent Loss Calculation is based on the formula which is included in report, in our case for Uniswap V3 we use a Monte Carlo Simulation.

2. Ethereum Price Prediction (ARIMA): Access the /predict_eth_price_arima endpoint to get Ethereum price predictions using an ARIMA model. The predicted price is available in JSON format. More info in readme file in AIML_Models folder.

3. Ethereum Price Prediction (LSTM): Access the /predict_eth_price_lstm endpoint. This endpoint utilizes Celery for asynchronous task execution. More info in readme file in AIML_Models folder.

Main Dependencies for Backend:
Flask: Web framework for building the API.
Celery: Distributed task queue for handling asynchronous tasks.
RabbitMQ: Message broker for Celery.
CORS: Cross-Origin Resource Sharing for handling cross-origin requests.
Certifi: Certificates for SSL verification.
NBconvert: Convert Jupyter Notebooks to Python scripts.
NBFormat: Format Jupyter Notebooks.
PythonEnv: Python virtual environment.