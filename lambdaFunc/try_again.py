
from __future__ import print_function

import sys

sys.path.append("verification/verification1/")


import helper         # file containing helper functions
import base           # the base class derived by all classes in derived    
import derived        # directory file containing imports for derived classes
import word_db        # dynamo-db wrapper class
import verification1  # simple verification model, always returns true
import phrase_generator
from verification1 import Verification

db = word_db.db()
pg = phrase_generator.phrase_generator()


class try_again(base.state_base):


    def __init__(self, task, word, sen_complete, def_complete, syn_complete, session_attributes):
        self.task = task
        self.word = word
        # These variables hold what tasks have already been completed
        self.sen_complete = sen_complete
        self.def_complete = def_complete
        self.syn_complete = syn_complete
        self.session_attributes = session_attributes
        
        
    def on_intent(self, intent_request, session):
        print("on_intent requestId=" + intent_request['requestId'] +
            ", sessionId=" + session['sessionId'])

        intent      = intent_request['intent']
        intent_name = intent_request['intent']['name']

        # Get user ID
        self.userId = session['user']['userId']
        print("userId=" + self.userId)
        
        if   intent_name == "agreeing_to_try_again":
            return self.intent_try_again()
        elif intent_name == "AMAZON.YesIntent":
            return self.intent_try_again()
        elif intent_name == "go_to_next_task":
            return self.intent_next_task()
        elif intent_name == "AMAZON.NoIntent":
            return self.intent_next_task()
        elif intent_name == "giving_an_answer_to_verify":
            return self.intent_verify(intent)
        elif intent_name == "give_an_example_answer":
            return self.intent_help()
        else:
            return self.base_intent_switch(intent, intent_name)
            
           
    def intent_try_again(self):
        session_attributes = {}
        card_title         = "Agree to Try Again"
        # Introduce the task attempt
        speech_output      = pg.generate(self.session_attributes, 'agreeing_to_try_again')
        reprompt_text      = "I'm ready for your input."
        should_end_session = False
        
        # Assign the next state
        self.session_attributes['state'] = {
            'value': 'attempt_task',
            'task' : self.task,
            'word' : self.word,
            'sen'  : self.sen_complete,
            'dfn'  : self.def_complete,
            'syn'  : self.syn_complete
        }
        # Populate prev_state
        self.session_attributes = helper.dump_state(self.session_attributes)
        
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session)) 
            
            
    def intent_next_task(self):
    
        card_title         = "Next Task after Fail"
        # Just use the value in the database
        speech_output      = pg.generate(self.session_attributes, 'go_to_next_task')
        should_end_session = False
        
        # Assign the next state
        self.session_attributes['state'] = {
            'value': 'select_task',
            'word' : self.word,
            'sen'  : self.sen_complete,
            'dfn'  : self.def_complete,
            'syn'  : self.syn_complete
        }
        # Dump the state to prev_state
        self.session_attributes = helper.dump_state(self.session_attributes)
        
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
            card_title, speech_output, None, should_end_session)) 
            
            
    def intent_verify(self, intent):

        # Get the answer from the intent
        answer = intent['slots']['ANSWER']['value']

        # Query the database for the correct answer set
        query = db.get_word_info(self.word)
        # Set the query to the value for this task
        query_task = query[self.task]
        # Set the query_syn to the synonym list of the word
        query_syn = query['syn']
        # Call the verification function with this info
        success = True

        try:
            verifier = Verification(self.word, query_syn, answer, query_task)
            if self.task == 'syn':
                success = verifier.synonym()
            if self.task == 'exa':
                success = verifier.sample()
            if self.task == 'def':
                success = verifier.definition()
        except:
            success = True
        

        self.session_attributes = self.session_attributes
        card_title = ""
        speech_output = ""
        should_end_session = False

        if (success):

            # Set the task as completed
            if (self.task == "syn"):
                self.syn_complete = '1'
            elif (self.task == "def"):
                self.def_complete = '1'
            else:
                self.sen_complete = '1'

            # Check to see if all tasks are completed
            if (self.sen_complete == '1' and self.def_complete == '1' and self.syn_complete == '1'):
                
                #Get User data
                words = (db.getUserData(self.userId))
                # Get a new word from the database
                self.word = db.get_random_word(self.userId)
                #update user info
                #db.addUserData(self.userId, self.word)

                # Update the word for the session attributes
                self.session_attributes['state']['word'] = self.word
                
                card_title = "Tasks Complete"
                speech_output = pg.generate(self.session_attributes, 'tasks_complete')
                reprompt_text = "Is this word satisfactory?"
                                
                # Initialize the select word class
                self.session_attributes['state'] = {
                    'value': 'select_word',
                    'word' : self.word
                }
                # Dump the state to prev_state
                self.session_attributes = helper.dump_state(self.session_attributes)

            # Move on to the next task for this word
            else:

                card_title = "Next Task"
                speech_output = pg.generate(self.session_attributes, 'next_task')
                reprompt_text = "Please choose a new task for this word."
                                            
                # Assign the next state
                self.session_attributes['state'] = {
                    'value': 'select_task',
                    'word' : self.word,
                    'sen'  : self.sen_complete,
                    'dfn'  : self.def_complete,
                    'syn'  : self.syn_complete
                }
                # Dump the state to prev_state
                self.session_attributes = helper.dump_state(self.session_attributes)

        # Prompt the user to try again
        else:
            card_title    = "Try Again"
            speech_output = pg.generate(self.session_attributes, 'try_again')
            reprompt_text = "Would you like to try again?"
            
            # Assign the next state            
            self.session_attributes['state'] = {
                'value': 'try_again',
                'task' : self.task,
                'word' : self.word,
                'sen'  : self.sen_complete,
                'dfn'  : self.def_complete,
                'syn'  : self.syn_complete
            }
            # Dump the state to prev_state
            self.session_attributes = helper.dump_state(self.session_attributes)

        # Return
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    
    
    # We redefine the help intent specifically for this module
    # Help will give an example here
    def intent_help(self):
    
        example = db.get_word_info(self.word)[self.task][0]
        #example = example[self.task]
    
        card_title         = "Example"
        # Just use the value in the database
        speech_output      = pg.generate(self.session_attributes, 'give_an_example_answer', example)
        should_end_session = False
        
        self.session_attributes = self.session_attributes
        
        return helper.build_response(self.session_attributes, helper.build_speechlet_response(
            card_title, speech_output, None, should_end_session)) 
