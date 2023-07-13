import os
import pandas
from nltk.tokenize import sent_tokenize

from src.utils.chatbot_utils import *
from src.utils.model_predictions import *
from src.utils.preprocessing_utils import *

class Chatbot:

    def __init__(self,req):
        self.req = req
        self.session_id = req['session_id']
        self.input_user = preprocess_text(req['message'])
        self.clear_conversation = req['clear_log']

    def response(self):
        # if self.clear_conversation:
        #     clear_log(self.session_id)
        # else:
            responses = []
            log_path = f"data/logs/chatbot_{self.session_id}.json"
            data_log = {
                "session_id": self.session_id,
                "input_user": self.input_user,
                "output_bot": None,
                "context": 'initial',
                "intents": [],
                "suposed_equipment":[],
                "suposed_issue":[],
                "equipment": None,
                "issue": None,
                "cause": None,
                "resolution": None
            }
            if not os.path.exists(log_path):
                log(self.session_id, data_log)
            else:
                pass
            context = get_log(self.session_id, 'context')
            if classifier_offensive(self.input_user) == True:
                responses.append(get_response('OFFENSIVE_TEXT'))
            else:
                suposed_equipment = classifier_equipament(self.input_user)
                if len(suposed_equipment) > 0:
                    responses.append(suposed_equipment[0]['text'])
                elif len(suposed_equipment) > 1:
                    list_equipment = []
                    for i in suposed_equipment:
                        list_equipment.append(i)
                    text = get_response('EQUIPMENT_IDENTIFICATION')
                    text = prepared_text(text,)
                    responses.append(text)
                else:
                    if 'motor' in self.input_user:
                        suposed_equipment = 'Motores elétricos'
                        responses.append(suposed_equipment)
                    elif 'caixa engrenagem' in self.input_user:
                        suposed_equipment = 'caixas de engrenagens'
                        responses.append(suposed_equipment)
                    else:
                        responses.append(get_response('FALLBACK_EQUIPAMENT'))

                
                suposed_issue = classifier_issue(self.input_user)
                if suposed_issue[0]['probability'] > 0.8:
                    issue = isolar_numero(suposed_issue[0]['class'])
                    responses.append(issue)

                else:
                    intent = classifier_intent(self.input_user)
                    if intent[0]['probability'] > 0.9:
                        responses.append(intent[0]['class'])

            response = []
            for i in responses:
                response.append({"text":i})
            return response
                    



                # try:
                #     if "QUESTION" in context:
                #         value_positive = verifiy_similarity(self.input_user)
                #         if value_positive == None:
                #             responses.append(get_response('FALLBACK_ANSWER'))
                #         elif value_positive == False:
                #             if context == "QUESTION_EQUIPMENT":
                #                 responses.append(get_response('FALLBACK_EQUIPAMENT'))
                #             elif context == "QUESTION_ISSUE":
                #                 responses.append(get_response('FALLBACK_PROBLEM'))
                #         else:
                #             if context == "QUESTION_EQUIPMENT":
                #                 equipment = get_log(self.session_id,"suposed_equipment")[0]
                #                 issue = None
                #                 context = "QUESTION_ISSUE"
                #             elif context == "QUESTION_ISSUE":
                #                 equipment = get_log(self.session_id,"equipment")
                #                 issue = get_log(self.session_id,"suposed_issue")[0]
                #                 context = "SOLUTION_ISSUE"

                #             data_log['equipment'] = equipment
                #             data_log['issue'] = issue
                #             data_log['context'] = context
                #             log(self.session_id,data_log)
                #     else:
                #         raise
                # except:
                    # equipment = get_log(self.session_id, 'equipment')
                    # issue = get_log(self.session_id, 'issue')

                    # if equipment != None and issue != None:
                    #     causes = get_cause_solution("cause", equipment, issue)
                    #     actions = get_cause_solution("action", equipment, issue)
                    #     resolutions = get_resolutions(causes, actions)
                    #     res1 = get_response('RESOLUTION_INTRODUCTION')
                    #     res1 = prepared_text(res1, issue, '$issue')
                    #     res2 = '#'.join(resolutions)
                    #     res = prepared_text(res1,res2,"$RESOLUTION_CAUSES").split('#')
                    #     for i in res:
                    #         responses.append(i)
                    # else:
                    #     tokens = sent_tokenize(self.input_user)
                    #     list_equipment = []
                    #     list_intent = []
                    #     list_issue = []
                    #     for token in tokens:         
                    #         intent = classifier_intent(token)
                    #         if intent['class'] != None:
                    #             list_intent.append(intent['class'])
                    #             data_log["intents"] = list_intent

                    #         if 'SAUDACAO' in list_intent and len(list_equipment) == 0 and len(list_issue) == 0 and equipment == None:
                    #             responses.append(get_response('WELCOME1'))
                    #             data_log["context"] = 'WELCOME'
                    #         else:
                    #             suposed_equipment = extract_main_equipment(token)
                    #             # suposed_equipment = (classifier_equipament(token))
                    #             if suposed_equipment['class'] != None:
                    #                 list_equipment.append(suposed_equipment['class'])
                    #                 data_log["suposed_equipment"] = list_equipment
                    #             suposed_issue = classifier_issue(token)
                    #             if suposed_issue['class'] != None:
                    #                 list_issue.append(suposed_issue['class'])
                    #                 data_log["suposed_issue"] = list_issue

                    #             if 'SAUDACAO' in list_intent and (len(list_equipment) > 0 or len(list_issue) > 0 or equipment != None):
                    #                 responses.append(get_response('WELCOME2'))

                    #             if len(list_issue) > 0 and len(list_equipment) == 0:
                    #                 responses.append(get_response('FALLBACK_EQUIPAMENT'))
                    #             else:
                    #                 if len(list_equipment) > 0 and equipment == None:
                    #                     text_res = get_response('CONFIRMATION_EQUIPMENT')
                    #                     res = prepared_text(text_res,suposed_equipment,'$')
                    #                     responses.append(res)
                    #                 else:
                    #                     if equipment != None and (len(list_issue) > 0 and issue == None):
                    #                         text_res = get_response('CONFIRMATION_ISSUE')
                    #                         res = prepared_text(text_res,suposed_issue,'$')
                    #                         responses.append(res)
                                
