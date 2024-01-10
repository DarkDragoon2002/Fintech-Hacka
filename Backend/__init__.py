from flask import Flask, jsonify, request
from flask_cors import CORS
from .main_routes import main
from .utils import celery_init_app

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["CELERY"] = {"broker_url": "pyamqp://guest:guest@localhost//", "result_backend": "rpc://"}
    celery = celery_init_app(app)

    app.register_blueprint(main)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
