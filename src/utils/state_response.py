from transitions import Machine
from random import choice
from model_predictions import *
from preprocessing_utils import *

class Conversation():
    with open(r'src\utils\data\contexts.txt', 'r') as arquivo:
        linhas = arquivo.readlines()
        contexts = [linha.strip() for linha in linhas]
        
    def __init__(self, message):
        self.message = message
        self.context = ''
        self.equipament = ''
        self.issue = ''
        self.intents = []

        self.machine = Machine(model=self, states=Conversation.contexts, initial='initial')
        for state in Conversation.contexts:
            self.machine.add_transition(trigger='...', source=state, dest='FALLBACK', conditions=['...'])
        self.machine.add_transition(trigger='PROBLEM_DESCRIPTION', source='PROBLEM_INDENTIFICATION', dest='FALLBACK', conditions=['...'])
        self.machine.add_transition(trigger='EQUIPMENT_DESCRIPTION', source='EQUIPMENT_INDENTIFICATION', dest='FALLBACK', conditions=['...'])

        self.machine.add_transition(trigger='GREETING', source='initial', dest='WELCOME', conditions=['começar conversa'])
        self.machine.add_transition(trigger='GREETING', source='initial', dest='WELCOME', conditions=['começar outra conversa'])

        self.machine.add_transition(trigger='...', source='initial', dest='ASSISTANCE', conditions=['...'])
        self.machine.add_transition(trigger='...', source='WELCOME', dest='ASSISTANCE', conditions=['...'])
        for state in Conversation.contexts:
            self.machine.add_transition(trigger='...', source=state, dest='ASSISTANCE', conditions=['outro problema'])

        self.machine.add_transition(trigger='PROBLEM_DESCRIPTION', source='initial', dest='EQUIPMENT_INDENTIFICATION', conditions=['...'])
        self.machine.add_transition(trigger='PROBLEM_DESCRIPTION', source='WELCOME', dest='EQUIPMENT_INDENTIFICATION', conditions=['...'])
        self.machine.add_transition(trigger='PROBLEM_DESCRIPTION', source='ASSISTANCE', dest='EQUIPMENT_INDENTIFICATION', conditions=['...'])
        self.machine.add_transition(trigger='PROBLEM_DESCRIPTION', source='FALLBACK', dest='EQUIPMENT_INDENTIFICATION', conditions=['...'])

        self.machine.add_transition(trigger='PROBLEM_DESCRIPTION', source='EQUIPMENT_INDENTIFICATION', dest='PROBLEM_INDENTIFICATION', conditions=['...'])
        self.machine.add_transition(trigger='PROBLEM_DESCRIPTION', source='FALLBACK', dest='PROBLEM_INDENTIFICATION', conditions=['...'])

        for state in Conversation.contexts:
            self.machine.add_transition(trigger='FAREWELL', source=state, dest='BYE', conditions=['...'])
        self.machine.add_transition(trigger='GRATITUDE', source=state, dest='BYE', conditions=['...'])

        self.machine.add_transition(trigger='...', source='PROBLEM_INDENTIFICATION', dest='PROBLEM_RESOLUTION', conditions=['...'])

        self.machine.add_transition(trigger='EXTRA_MATERIAL_REQUEST', source='PROBLEM_RESOLUTION', dest='EXTRA_MATERIAL_REQUEST')

        self.machine.add_transition(trigger='DOUBT', source='PROBLEM_RESOLUTION', dest='INFORMATION_REQUEST')

        for state in Conversation.contexts:
            self.machine.add_transition(trigger='FEEDBACK', source=state, dest='FEEDBACK')
        
        for state in Conversation.contexts:
            self.machine.add_transition(trigger='SMALL_TALK', source=state, dest='SMALL_TALK')
        


    @staticmethod
    def _get_response(context,key):
        with open(r'..\database\responses\responses.json','r') as f:
            response = choice(f[context][key])
        return response
    
    @staticmethod
    def _get_intents(self):
        intents = classifier_intent(self.message)
        return intents
    
    # @staticmethod
    # def _get_entities(self):
    #     entities = classifier_entities(self.message)
    #     return entities
    
    @staticmethod
    def _get_equipment(self):
        equipament = classifier_equipament(self.message)
        return equipament
    
    @staticmethod
    def _get_issue(self):
        issue = classifier_issue(self.message)
        return issue
    
    @staticmethod
    def _get_solution(self):
        ...
