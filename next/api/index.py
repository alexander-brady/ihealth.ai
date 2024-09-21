from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/api/query", methods=["POST"])
def post_query():
    data = request.json  
    query = data.get('query')
    return jsonify({"response": "Hello World"})