
from __future__ import print_function

import sys

sys.path.append("verification/verification1/")

import main
import helper         # file containing helper functions
import base           # the base class derived by all classes in derived    
import derived        # directory file containing imports for derived classes
import word_db        # dynamo-db wrapper class
import verification1  # simple verification model, always returns true
import phrase_generator

pg = phrase_generator.phrase_generator()

class select_word(base.state_base):
        
    def on_intent(self, intent_request, session):
        print("on_intent requestId=" + intent_request['requestId'] +
            ", sessionId=" + session['sessionId'])
        print ('select_word')

        intent      = intent_request['intent']
        intent_name = intent_request['intent']['name']

        # Get user ID
        self.userId = session['user']['userId']
        print("userId=" + self.userId)
        
        if   intent_name == "AMAZON.YesIntent":
            return self.intent_word_confirmed(intent)
        elif intent_name == "specifying_a_task":
            return self.intent_task_specified(intent)
        elif intent_name == "AMAZON.NoIntent":
            return self.intent_word_skipped(intent)
        else:
            return self.base_intent_switch(intent, intent_name)
            
            
    def intent_word_confirmed(self, intent):
        
        card_title         = "Word Confirmed"
        speech_output      = pg.generate(self.session_attributes, 'confirming_word')
        reprompt_text      = "Please select a task."
        should_end_session = False
        
        # Assign the next state
        self.session_attributes['state'] = {
            'value': 'select_task',
            'word' : self.word,
            'sen'  : '0',
            'dfn'  : '0',
            'syn'  : '0'
        }
        # Populate prev_state
        self.session_attributes = helper.dump_state(self.session_attributes)
        
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
    
    
    def intent_task_specified(self, intent):
    
        resolution = intent['slots']['TASK']['resolutions']['resolutionsPerAuthority'][0]
        values = resolution['values'][0]
        task = values['value']['id']
        
        # Store task preemptively to pass to pg.generate
        self.session_attributes['state']['task'] = task
    
        card_title         = "Task Chosen"
        speech_output      = pg.generate(self.session_attributes, 'specifying_a_task')
        reprompt_text      = "I'm ready for your input."
        should_end_session = False
        
        # Assign the next state
        self.session_attributes['state'] = {
            'value': 'attempt_task',
            'task' : task,
            'word' : self.word,
            'sen'  : '0',
            'dfn'  : '0',
            'syn'  : '0'
        }
        # Populate prev state
        self.session_attributes = helper.dump_state(self.session_attributes)
        
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
    
    
    
