import os
import json
from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
from flask_cors import CORS, cross_origin
from main import Chatbot

app = Flask(__name__)
app.config['SECRET_KEY'] = '<V"~WY6une=>Pzue9{-k&~R?+w\?NkeC'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app)

@app.route('/chat', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def chat():
    req = request.get_json()
    session_id = session.get('session_id')
    input_user = req['message']
    clear_log = req['clear_log']

    message = {
        'session_id': session_id,
        'message': input_user,
        'clear_log': clear_log
    }

    response_message = Chatbot(message)
    response_message = response_message.response()
    response = jsonify(response_message)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

@app.route('/', methods=['GET'])
def index():
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
