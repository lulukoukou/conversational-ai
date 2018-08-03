
from __future__ import print_function

import sys

sys.path.append("verification/verification1/")

import helper         # file containing helper functions
import base           # the base class derived by all classes in derived    
import derived        # directory file containing imports for derived classes
import word_db        # dynamo-db wrapper class
import verification1  # simple verification model, always returns true
import phrase_generator

pg = phrase_generator.phrase_generator()

class select_task(base.state_base):

    def __init__(self, word, sen_complete, def_complete, syn_complete, session_attributes):
        self.word = word
        self.sen_complete = sen_complete
        self.def_complete = def_complete
        self.syn_complete = syn_complete
        self.session_attributes = session_attributes
        
    def on_intent(self, intent_request, session):
        print("on_intent requestId=" + intent_request['requestId'] +
            ", sessionId=" + session['sessionId'])
        print ('select_task')

        intent      = intent_request['intent']
        intent_name = intent_request['intent']['name']

        # Get user ID
        self.userId = session['user']['userId']
        print("userId=" + self.userId)
        
        if   intent_name == "what_are_the_tasks":
            return self.intent_help()
        elif intent_name == "specifying_a_task":
            return self.intent_task_specified(intent)
        else:
            return self.base_intent_switch(intent, intent_name)
            
            
    def intent_help(self):
        
        card_title         = "Repeat Tasks"
        speech_output      = pg.generate(self.session_attributes, 'what_are_the_tasks')
        should_end_session = False
        
        # Stay in state
        self.session_attributes = self.session_attributes
        
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
            card_title, speech_output, None, should_end_session)) 
            
            
    def intent_task_specified(self, intent):
    
        # check to see if we parsed a value
        content_present = intent['slots']['TASK'].get('resolutions')
        task = None
        if content_present:
            resolution = intent['slots']['TASK']['resolutions']['resolutionsPerAuthority'][0]
            # if we have a task match
            if resolution.get('values'):
                values = resolution['values'][0]
                task = values['value']['id']
        
        # caught an incorrect value
        if task == None:
        
            self.session_attributes = self.session_attributes
        
            card_title         = "Invalid Task"
            speech_output      = "We could not understand your exercise. Could you please repeat?"
            should_end_session = False
            
            return helper.build_response(self.session_attributes, helper.build_speechlet_response(
                card_title, speech_output, None, should_end_session))   
        
        
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
            'sen'  : self.sen_complete,
            'dfn'  : self.def_complete,
            'syn'  : self.syn_complete
        }
        # Populate prev_state
        self.session_attributes = helper.dump_state(self.session_attributes)
        
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))        
    
