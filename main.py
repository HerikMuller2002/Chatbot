import os
import pandas
from nltk.tokenize import sent_tokenize

from src.utils.chatbot_utils import *
from src.utils.model_predictions import *

class Chatbot:

    def __init__(self,req):
        self.req = req
        self.session_id = req['session_id']
        self.input_user = req['message']
        self.clear_conversation = req['clear_log']

    def response(self):
        if self.clear_conversation == True:
            try:
                os.remove(f'data\logs\log_{self.session_id}')
            except OSError as erro:
                print(f"Erro ao excluir o arquivo: data\logs\log_{self.session_id}\n{erro}")
        else:
            responses = []
            if filter_censure(self.input_user) == True:
                responses.append(get_response('OFFENSIVE_TEXT'))
            else:
                tokens = sent_tokenize(self.input_user)
                list_equipament = []
                list_intent = []
                list_problem = []
                for token in tokens:
                    equipament = (classifier_equipament(token))
                    if equipament:
                        list_equipament.append([equip['class'] for equip in equipament])

                    intent = classifier_intent(token)
                    if intent['class'] != None:
                        list_intent.append(intent['class'])

                    problem = classifier_problem(token)
                    if problem['class'] != None:
                        list_problem.append(problem['class'])

                if 'SAUDACAO' in list_intent and len(list_equipament) == 0 and len(list_problem) == 0:
                    responses.append(get_response('WELCOME1'))
                else:
                    if 'SAUDACAO' in list_intent and (len(list_equipament) > 0 or len(list_problem) > 0):
                        responses.append(get_response('WELCOME2'))
                    if len(list_problem) > 0 and len(list_equipament) == 0:
                        responses.append(get_response('FALLBACK_EQUIPAMENT'))
                    else:
                        if len(list_equipament) > 0 and len(list_problem) == 0:
                            responses.append(get_response('FALLBACK_PROBLEM'))
                        else:
                            if 'FEEDBACK_NEGATIVO' in list_intent:
                                responses.append(get_response('NEGATIVE_FEEDBACK'))
                            else:
                                if 'DESPEDIDA' in list_intent and len(list_equipament) == 0 and len(list_problem) == 0:
                                    responses.append(get_response('GOODBYE'))
                                else:
                                    if 'PEDIDO_AJUDA' in list_intent and len(list_equipament) == 0 and len(list_problem) == 0:
                                        responses.append(get_response('SERVICE_REQUEST'))
                                    else:
                                        if 'AGRADECIMENTO' in list_intent and len(list_equipament) == 0 and len(list_problem) == 0:
                                            responses.append(get_response('THANKS'))
                                        else:
                                            responses.append(get_response('FALLBACK'))
                
                df = pd.read_excel(r"src\utils\data\num_problems.xlsx")
                for trouble in list_problem:
                    line = df.loc[df['problem'] == trouble]
                    for equip in list_equipament:
                        if equip[0].lower() == str(line['class'].item()).lower():
                            responses = [""]
                        else:
                            responses = [get_response('FALLBACK_PROBLEM')]
            response = []
            for i in responses:
                response.append({"text":i})
            return response