import os
import json
from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
from flask_cors import CORS, cross_origin

# import main

app = Flask(__name__)
app.config['SECRET_KEY'] = '<V"~WY6une=>Pzue9{-k&~R?+w\?NkeC'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app, resources={r"/test": {"origins": "http://localhost:5550"}})

@app.route('/test', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def test():
    req = request.get_json()
    session_id = session.get('session_id')
    input_user = req['message']

    message = {
        'session_id': session_id,
        'message': input_user
    }

    # response_message = main(message)
    # response = jsonify(response_message)

    response = [{'text': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'}]
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

@app.route('/', methods=['GET'])
def index():
    session['session_id'] = os.urandom(16).hex()
    return render_template('index.html')

if __name__ == '__main__':
    # os.makedirs(LOGS_DIR, exist_ok=True)
    # app.run(port=4000, debug=True)
    app.run(host='127.0.0.1', debug=True)