from flask import Flask, request, jsonify, redirect, url_for
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy

import os


app = Flask(__name__)
Swagger(app)


@app.route('/')
def index():
    return redirect('/apidocs/')


@app.route('/answer', methods=['GET'])
def answer():
    """
    Generate ChitChat answer to user phrase for session
    ---
    parameters:
      - name: q
        in: query
        required: true
        type: string
      - name: session
        in: query
        required: true
        type: string
    """
    q = request.args.get('q')
    id = request.args.get('session')
    with ClusterRpcProxy({'AMQP_URI': os.environ['AMQP_URI']}) as rpc:
        a = rpc.chitchat.predict(q, id)

    result = {
        'session': id,
        'question': q,
        'answer': a
    }
    return jsonify(result), 200


@app.route('/init_session', methods=['GET'])
def init_session():
    """
    Init new or reset existing user session
    ---
    parameters:
      - name: session
        in: query
        required: true
        type: string
    """
    id = request.args.get('session')
    with ClusterRpcProxy({'AMQP_URI': os.environ['AMQP_URI']}) as rpc:
        a = rpc.chitchat.init_session(id)

    result = {
        'session': id
    }
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
