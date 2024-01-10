The API is built using Flask, which is a Python Framework and integrates Celery for handling asynchronous tasks.

Features
1. Impermanent Loss Prediction: Utilize the /predict_impermanent_loss endpoint to predict Impermanent Loss based on specified parameters such as Range Percentage, Mean, and Standard Deviation. Impermanent Loss Calculation is based on the formula which is included in report, in our case for Uniswap V3 we use a Monte Carlo Simulation.

2. Ethereum Price Prediction (ARIMA): Access the /predict_eth_price_arima endpoint to get Ethereum price predictions using an ARIMA model. The predicted price is available in JSON format. More info in readme file in AIML_Models folder.

3. Ethereum Price Prediction (LSTM): Trigger Ethereum price prediction using LSTM by making a request to the /predict_eth_price_lstm endpoint. This endpoint utilizes Celery for asynchronous task execution. More info in readme file in AIML_Models folder.

Scheduled Task: The API supports scheduled tasks, demonstrated in the /task endpoint, showcasing a continuous background task.

Explore the various endpoints like /predict_impermanent_loss, /predict_eth_price_arima, and /predict_eth_price_lstm. Schedule tasks (for the LSTM model as it requires more processing and a longer duration) using asynchronous task scheduling.

Main Dependencies for Backend:
Flask: Web framework for building the API.
Celery: Distributed task queue for handling asynchronous tasks.
RabbitMQ: Message broker for Celery.
CORS: Cross-Origin Resource Sharing for handling cross-origin requests.
Certifi: Certificates for SSL verification.
NBconvert: Convert Jupyter Notebooks to Python scripts.
NBFormat: Format Jupyter Notebooks.
PythonEnv: Python virtual environment.