#!/usr/bin/env python3


from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/json')
def json_example():
    data = {"message": "Hello, World!"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
