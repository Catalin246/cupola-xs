from flask import Flask, jsonify

app = Flask(__name__)

# This is only a test route. Must be removed when we start building the API.
@app.route('/')
def index():
    return jsonify({"message": "Hello World!"})