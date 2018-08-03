from __future__ import print_function

import sys

sys.path.append("verification/verification1/")

import helper   # file containing helper functions
import base     # file containing the base class
import derived  # directory file containing imports for derived classes
import word_db

# --------------- Globals ------------------

# Global variable holding the conversation state
# (the variable in which the state classes are initialized)
state = None


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return helper.get_welcome_response(session)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    # This call is safe to session_attributes not being defined.
    # It should only apply during initialization.
    session_attributes = event['session'].get('attributes')
          
    # print ("session_attributes in main = " + str(session_attributes))
      
    # assign the state based on the values in the session attributes
    state = helper.set_state(session_attributes)
    
    # print ("state in main = " + str(state))
    
    # set up the session
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    # decide what to do
    if   event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return state.on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
        
