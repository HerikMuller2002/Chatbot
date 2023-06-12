import sys, os
# sys.path.append(os.path.abspath(os.path.join('..', 'Chatbot\\main')))
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/test": {"origins": "http://localhost:5550/"}})

@app.route('/test', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def index():
    req = request.get_json()
    # message = chatbot_run(req['message'])
    message = [{'text':'oi'}]
    response = jsonify(message)
    
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

@app.route('/', methods=['GET'])
def index2():
    return render_template('index.html')

if __name__ == '__main__':
    # app.run(port=5000, debug=True)
    app.run(port=4000, debug=True)