from nbconvert import PythonExporter
import nbformat

def execute_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb_content = f.read()
    
    notebook = nbformat.reads(nb_content, as_version=4)
    exporter = PythonExporter()
    (python_code, _) = exporter.from_notebook_node(notebook)

    exec(python_code, globals())