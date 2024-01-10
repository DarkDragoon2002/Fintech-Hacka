from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from celery import Celery, shared_task
from celery.contrib.abortable import AbortableTask
import time

from .exec_notebook import execute_notebook

# celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@shared_task(bind=True, base=AbortableTask)
def price_task(self):
    notebook_path = '../AIML_Models/MultivariateLSTM_withSentiment.ipynb'
    global task_result
    task_result = None

    if request.method == 'POST':
        output = execute_notebook(notebook_path)

        while output is None:
            time.sleep(10)
            continue

        with open('result_lstm.txt', 'r') as file:
            result_content = file.read()
            json_output = jsonify({'Predicted Price': result_content})

    task_result = json_output



