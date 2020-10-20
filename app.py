from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route("/")
def index():
    return {
        'hello':'world'
    }
    
if __name__ == "__main__":    
    app.run()