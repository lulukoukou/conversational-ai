
from __future__ import print_function

import helper
import word_db
import helper
import phrase_generator
# This file contains the base class definition.
# The base class will never be instantiated.
pg = phrase_generator.phrase_generator()
db = word_db.db()

class state_base:
   
    # Get word, passed as input
    def __init__(self, word, session_attributes):
        self.word = word
        self.session_attributes = session_attributes
        self.userId = None
   
    # Base intent handler, calls base intent switch
    def on_intent(self, intent_request, session):
        print("on_intent requestId=" + intent_request['requestId'] +
            ", sessionId=" + session['sessionId'])
    
        intent      = intent_request['intent']
        intent_name = intent_request['intent']['name']

        # Get user ID
        self.userId = session['user']['userId']
        print("userId=" + self.userId)
    
        return self.base_intent_switch(intent, intent_name)


    # These handlers are defined inside the base class.
    # They may be redefined in derived classes.
    def base_intent_switch(self, intent, intent_name): 
    
        if   intent_name == "skip_word":
            return self.intent_word_skipped(intent)
        elif intent_name == "AMAZON.HelpIntent":
            return self.intent_help()
        elif intent_name == "AMAZON.CancelIntent":
            return self.intent_cancel()
        elif intent_name == "AMAZON.StopIntent":
            return self.intent_exit()
        else:
            return self.intent_unhandled()
         
         
    # When the user wants to skip the current word (for whatever reason) this is called
    def intent_word_skipped(self, intent):
     
        #Get User data
        words = db.getUserData(self.userId)
        # Get a new word from the database
        word = db.get_random_word(self.userId)
        #update user info
        #db.addUserData(self.userId, word)
        
        # Assign that word to the state before passing to speech_output
        self.session_attributes['state']['word'] = word
    
        card_title         = "Word Skipped"
        speech_output      = pg.generate(self.session_attributes, 'skip_word')
        reprompt_text      = "Is this word satisfactory?"
        should_end_session = False
        
        # Initialize the select word class
        self.session_attributes['state'] = {
            'value': 'select_word',
            'word' : word
        }
        # Dump the state to prev_state
        self.session_attributes = helper.dump_state(self.session_attributes)
        
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
    
         
    # Help will be redefined in various derived classes. Here, it only prompts
    # the user with how to exit.
    def intent_help(self):
        card_title         = "Help"
        speech_output      = pg.generate(self.session_attributes, 'help')
        should_end_session = False
        
        self.session_attributes = self.session_attributes
        
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
                card_title, speech_output, None, should_end_session))
        
    # Cancel intent is assumed to mean the user wants to return to the previous
    # state. It may be reassigned in the future.
    def intent_cancel(self):
        card_title         = "Cancel"
        speech_output      = "Bringing you back to the previous step"
        should_end_session = False
        
        # Go back to the last state
        self.session_attributes['state'] = self.session_attributes['prev_state']
        
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
                card_title, speech_output, None, should_end_session))
        
    # This is the exit intent, and calls the session ending function
    def intent_exit(self):
        card_title         = "Session Ended"
        speech_output      = pg.generate(self.session_attributes, 'stop')
        # Setting this to true ends the session and exits the skill.
        should_end_session = True
        return helper.build_response({}, helper.build_speechlet_response(
                card_title, speech_output, None, should_end_session))
        
        
    def intent_unhandled(self):
      
        card_title    = "Unhandled Intent"
        speech_output = (
                            "We weren't able to understand what you were saying. " + 
                            "Would you mind saying it another way?"
                        )
        reprompt_text = (
                            "We still weren't able to understand what you were saying. " + 
                            "Please say it another way."
                        )
        should_end_session = False
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        
        
        
        
