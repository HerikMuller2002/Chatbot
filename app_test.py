import os
import json
from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app, resources={r"/test": {"origins": "http://localhost:5550"}})

LOGS_DIR = 'logs'  # Diretório para armazenar os logs

@app.route('/test', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def test():
    req = request.get_json()
    session_id = session.get('session_id')
    message = req['message']

    log_data = {
        'session_id': session_id,
        'message': message
    }
    log_filename = f'{session_id}.json'
    log_filepath = os.path.join(LOGS_DIR, log_filename)

    with open(log_filepath, 'a') as log_file:
        log_file.write(json.dumps(log_data) + '\n')

    # message = chatbot_run(message)
    response = jsonify({'text': 'Oi'})
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

@app.route('/', methods=['GET'])
def index():
    session['session_id'] = os.urandom(16).hex()
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(LOGS_DIR, exist_ok=True)  # Cria a pasta 'logs' se ela não existir
    app.run(port=4000, debug=True)
