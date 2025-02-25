import os
from flask import Flask
from routes import api_blueprint
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "data"
CORS(app)  

app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
