
from __future__ import print_function

import sys

sys.path.append("verification/verification1/")

import base           # the base class derived by all classes in derived    
import derived        # directory file containing imports for derived classes
import word_db        # dynamo-db wrapper class
import verification1  # simple verification model, always returns true
import phrase_generator

import select_word
import select_task
import attempt_task
import try_again

# Instantiate the database API

pg = phrase_generator.phrase_generator()
db = word_db.db()

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

    
# --------------- Helpers that interact with the session attributes ------------   

# Use the session attributes to set the state of the system. If there are none,
# assume no state.
def set_state(session_attributes):
    
    # print ("session_attributes in set_state = " + str(session_attributes))
    
    temp_state = None
    
    if (session_attributes):
        next_state = session_attributes['state']['value']
    
        if   (next_state == 'select_word'):
            word  = session_attributes['state']['word']
            temp_state = select_word.select_word(word, session_attributes)
            
        elif (next_state == 'select_task'):
            word  = session_attributes['state']['word']
            sen   = session_attributes['state']['sen']
            dfn   = session_attributes['state']['dfn']
            syn   = session_attributes['state']['syn']
            temp_state = select_task.select_task(word, sen, dfn, syn, session_attributes)
            
        elif (next_state == 'attempt_task'):
            task  = session_attributes['state']['task']
            word  = session_attributes['state']['word']
            sen   = session_attributes['state']['sen']
            dfn   = session_attributes['state']['dfn']
            syn   = session_attributes['state']['syn']
            temp_state = attempt_task.attempt_task(task, word, sen, dfn, syn, session_attributes)
            
        elif (next_state == 'try_again'):
            task  = session_attributes['state']['task']
            word  = session_attributes['state']['word']
            sen   = session_attributes['state']['sen']
            dfn   = session_attributes['state']['dfn']
            syn   = session_attributes['state']['syn']
            temp_state = try_again.try_again(task, word, sen, dfn, syn, session_attributes)
        
    # print ("state in helper = " + str(state))
    
    return temp_state

# populate the session attributes with a dictionary describing
# the current state (which will become the previous state)
def dump_state(session_attributes):
    
    session_attributes['prev_state'] = session_attributes['state']
    
    return session_attributes

    
# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response(session):

    # Get user ID
    userId = session['user']['userId']
    print("userId=" + userId)
    #Get User data
    #words = (db.getUserData(userId))
    # Get the first word from the DB
    db.delUserData(userId)
    word = db.get_random_word(userId)
    #update user info
    #db.addUserData(userId, word)

    # Set up the session_attributes to contain the starting state
    # (makes word_generator easier)
    session_attributes = { 'state': { 'value': 'welcome', 'word': word}}
    
    card_title         = "Welcome"
    speech_output      = pg.generate(session_attributes)
    reprompt_text      = "Is this work satisfactory?"
    should_end_session = False
    
    # Initialize the select word class
    session_attributes['state'] = {
        'value': 'select_word',
        'word' : word
    }
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
