from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS

from .imp_loss import calcExpImpLoss
from .exec_notebook import execute_notebook, execute_notebook_input
from .tasks import price_task

from nbconvert import PythonExporter
import nbformat
import certifi

ca_file = certifi.where()

main = Blueprint('main', __name__)

# # Start the scheduled task, which is imported from the exec_noterbook.py file (change target later!)
# def start_scheduled_task():
#     task_thread = threading.Thread(target=task)
#     task_thread.daemon = True  # Daemonize the thread
#     task_thread.start()
#     return task_thread

@main.route('/', methods=['GET'])
def index():
    return jsonify({'Message': 'Welcome to the NUS Fintech Hackathon API!'})

@main.route('/predict_impermanent_loss', methods=['GET', 'POST'])
def predict_impermanent_loss():
    json_data = {
        "note": "Send a POST request in JSON format with the following parameters: rangePerc: Range Percentage, mu: Mean, sigma: Standard Deviation to get the predicted Impermanent Loss!"
    }
    if request.method == 'GET':
        return jsonify(json_data)
    
    if request.method == 'POST':
        json_data = request.get_json()

        rangePerc = json_data['rangePerc']
        mu = json_data['mu']
        sigma = json_data['sigma']

        impLoss = calcExpImpLoss(float(rangePerc), float(mu), float(sigma))
        return jsonify({'Predicted Impermanent Loss': impLoss}), 200

@main.route('/predict_eth_price_arima', methods=['GET'])
def predict_eth_price_arima():
    notebook_path = '../AIML_Models/ARIMA for API Integration.ipynb'
    execute_notebook(notebook_path)
    
    with open('result_arima.txt', 'r') as file:
        result_content = file.read()
        json_output = jsonify({'Predicted Price': result_content})
    
    return json_output, 200

@main.route('/predict_eth_price_lstm', methods=['GET'])
def predict_eth_price_lstm():
    result = price_task.delay()
    return jsonify({'Task': 'Triggered', 'Task ID': result.id}), 200

    



    
            