from nbconvert import PythonExporter
import nbformat
import threading

def execute_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb_content = f.read()
    
    notebook = nbformat.reads(nb_content, as_version=4)
    exporter = PythonExporter()
    (python_code, _) = exporter.from_notebook_node(notebook)

    exec(python_code, globals())

def execute_notebook_input(notebook_path, **kwargs):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb_content = f.read()
    
    notebook = nbformat.reads(nb_content, as_version=4)
    exporter = PythonExporter()
    (python_code, _) = exporter.from_notebook_node(notebook)

    input_coin = kwargs.get('input_value')

    if input_coin is not None:
        python_code += f"\nARIMA_Function({input_coin})"

    exec(python_code, globals())