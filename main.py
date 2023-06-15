import os
from src.utils.chatbot_utils import *

class Chatbot:

    def __init__(self,req):
        self.req = req
        self.session_id = req['session_id']
        self.input_user = req['message']
        self.clear_conversation = req['clear_log']

    def get_response(self):
        if self.clear_conversation == True:
            try:
                os.remove(f'data\logs\log_{self.session_id}')
            except OSError as erro:
                print(f"Erro ao excluir o arquivo: data\logs\log_{self.session_id}\n{erro}")
        else:
            if filter_censure(self.input_user) == True:
                response = ...
                return response
            else:
                ...
                response =...





message = {
        'session_id': 123,
        'message': 'olá',
        'clear': True
    }

Chatbot(message)