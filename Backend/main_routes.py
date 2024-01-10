from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS

from .imp_loss import calcExpImpLoss
from .exec_notebook import execute_notebook

from nbconvert import PythonExporter
import nbformat
import certifi

ca_file = certifi.where()

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return jsonify({'Message': 'Welcome to the NUS Fintech Hackathon API!'})

@main.route('/predict_impermanent_loss', methods=['GET', 'POST'])
def predict_impermanent_loss():
    json_data = {
        "Message": "There is nth here get fucked!",
    }
    if request.method == 'GET':
        return jsonify(json_data)
    
    if request.method == 'POST':
        json_data = request.get_json()

        rangePerc = json_data['rangePerc']
        mu = json_data['mu']
        sigma = json_data['sigma']

        impLoss = calcExpImpLoss(float(rangePerc), float(mu), float(sigma))
        return jsonify({'Predicted Impermanent Loss': impLoss})

@main.route('/predict_eth_price_arima', methods=['GET'])
def predict_eth_price_arima():
    notebook_path = '../AIML_Models/ARIMA for API Integration.ipynb'
    execute_notebook(notebook_path)
    
    with open('result.txt', 'r') as file:
        result_content = file.read()
        # Assuming result_content is a JSON-serializable string, convert to JSON
        json_output = jsonify({'Predicted Price': result_content})
    
    return json_output

# @main.route('/predict_eth_price_lstm', methods=['GET'])
# def predict_eth_price_lstm():
#     notebook_path = 'LSTM.ipynb'
#     output = execute_notebook(notebook_path)
#     return jsonify(output)

# @main.route('/predict_eth_price_multivariatelstm', methods=['GET', 'POST'])
# def predict_eth_price_multivariatelstm():
#     notebook_path = 'LSTM.ipynb'
#     output = execute_notebook(notebook_path)
#     return jsonify(output)

            