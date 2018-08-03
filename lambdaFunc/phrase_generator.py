
from __future__ import print_function

import helper
import word_db
import helper

import random

# This class contains the word generator code.
# It mostly amounts to a nested dictionary that contains reasonable
# sentences based on the current state.

# Usage: word_generator.generate(session_attributes)

class phrase_generator():

    # Set up the nested dictionary
    def __init__(self):
        
        self.data = {
            'welcome': {
                'default': {
                    "Welcome to Say Hello! Let's start broadening your vocabulary. Your first word today is [WORD]. Is that good?",
                    "Welcome to Say Hello! I'll help you with your English vocabulary. Your first word is [WORD]. Sound good?",
                    "Welcome to Say Hello! Let's build your vocabulary. Your word is [WORD]. Is that alright?"
                }
            },
            'select_word': {
                'skip_word': {
                    "Ok, your new word is [WORD]. Is this word satisfactory?" ,
                    "I'll find a better word for you. How's [WORD]?",
                    "How about [WORD]?",
                    "Don't be too picky. Let's try [WORD]."
                },
                'confirming_word': {
                    "You've confirmed the word [WORD]. What exercise do you want to start with?",
                    "You've confirmed the word [WORD]. Tell me which exercise you want.",
                    "[WORD] it is. What exercise do you want to start with?",
                    "[WORD] it is. Tell me which exercise you want.",
                    "Good choice. What exercise do you want to start with?",
                    "Good choice. Tell me which exercise you want."
                },
                'specifying_a_task': {
                    "Alright, we'll do a [TASK]. I'm ready when you are.",
                    "Okay, I'm ready.",
                    "Ready when you are.",
                    "Let's begin."
                },
                'help': {
                    "You may exit the program at any time by saying exit.",
                    "If you like the word [WORD], just say yes.",
                    "If you don't like the current word, say skip."
                },
                'stop': {
                    "Exiting now",
                    "Goodbye!",
                    "Thanks for using Say Hello!"
                }
            },
            'select_task': {
                'skip_word': {
                    "Okay I'll change your word. Your next word is [WORD]",
                    "Alright, Let's move on to a new word. Your next word is [WORD]"
                },
                'specifying_a_task': {
                    "Alright, we'll do a [TASK]. I'm ready when you are.",
                    "Okay, I'm ready.",
                    "Ready when you are.",
                    "Let's begin."
                },
                'what_are_the_tasks': {
                    "You can do three types of exercises. You can tell me the definition of the word, use the word in a sentence, or tell me some synonyms for the word. Which sounds good?",
                    "These are the three options: Give the definition of the word, provide a sentence containing the word, or give a synonym for the word. Which would you like?"
                },
                'help': {
                    "You may exit the program at any time by saying exit.",
                    "If you're unsure which tasks are available, just ask.",
                    "If you don't like the current word, you can always skip it."
                },
                'stop': {
                    "Exiting now",
                    "Goodbye!",
                    "Thanks for using Say Hello!"
                }
            },
            'attempt_task': {
                'skip_word': {
                    "Okay I'll change your word. Your next word is [WORD]",
                    "Alright, Let's move on to a new word. Your next word is [WORD]"
                },
                'exa': {
                    "I'm happy to help clarify. A [TASK] for [WORD] is [WORD_INFO].",
                    "[WORD_INFO] is a sentence [WORD] could be used in."
                },
                'syn': {
                    "I'm happy to help clarify. A [TASK] for [WORD] is [WORD_INFO].",
                    "Another way to say [WORD] is [WORD_INFO].",
                    "Another word for [WORD] is [WORD_INFO].",
                    "An example synonym of [WORD] is [WORD_INFO]."
                },
                'def': {
                    "I'm happy to help clarify. A [TASK] for [WORD] is [WORD_INFO].",
                    "[WORD] means [WORD_INFO]."
                },
                'tasks_complete': {
                    "You got it! Congruatulations, you've completed all the exercises for this word! Your new word is [WORD]. Is that good?",
                    "Great job! You've completed all the exercises for this word! Your new word is [WORD].",
                    "Great job! You've completed all the exercises for this word! Your new word is [WORD]. Is that good?",
                    "Excellent! That completes the exerecises for this word. Your next word is [WORD].",
                    "That's all the exercises for this word. Is [WORD] a good next word?"
                },
                'next_task': {
                    "You got it! Please choose another exercise for this word.",
                    "Great job! Now, choose another exercise.",
                    "Great job! Which exercise would you like next?",
                    "Excellent! Now, choose another task for this word please.",
                    "Nice work. Which exercise would you like next?"
                },
                'try_again': {
                    "There might be some better answer. Would you like to try again?",
                    "Unfortunately not. Want to try again?",
                    "That's incorrect. Do you want to try again?",
                    "I'm sorry but I think there might be a better answer. Want to try again?"
                },
                'stop': {
                    "Exiting now",
                    "Goodbye!",
                    "Thanks for using Say Hello!"
                }
            },
            'try_again': {
                'skip_word': {
                    "That's okay! You can always come back to practice this word again. Your new word is [WORD]."
                },
                'exa': {
                    "I'm happy to help clarify. A [TASK] for [WORD] is [WORD_INFO].",
                    "[WORD_INFO] is a sentence [WORD] could be used in."
                },
                'syn': {
                    "I'm happy to help clarify. A [TASK] for [WORD] is [WORD_INFO].",
                    "Another way to say [WORD] is [WORD_INFO].",
                    "Another word for [WORD] is [WORD_INFO].",
                    "An example synonym of [WORD] is [WORD_INFO]."
                },
                'def': {
                    "I'm happy to help clarify. A [TASK] for [WORD] is [WORD_INFO].",
                    "[WORD] means [WORD_INFO]."
                },
                'tasks_complete': {
                    "You got it! Congruatulations, you've completed all the exercises for this word! Your new word is [WORD]. Is that good?",
                    "Great job! You've completed all the exercises for this word! Your new word is [WORD].",
                    "Great job! You've completed all the exercises for this word! Your new word is [WORD]. Is that good?",
                    "Excellent! That completes the exerecises for this word. Your next word is [WORD].",
                    "That's all the exercises for this word. Is [WORD] a good next word?"
                },
                'next_task': {
                    "You got it! Please choose another exercise for this word.",
                    "Great job! Now, choose another exercise.",
                    "Great job! Which exercise would you like next?",
                    "Excellent! Now, choose another task for this word please.",
                    "Nice work. Which exercise would you like next?"
                },
                'try_again': {
                    "There might be some better answer. Would you like to try again?",
                    "Unfortunately not. Want to try again?",
                    "That's incorrect. Do you want to try again?",
                    "I'm sorry but I think there might be a better answer. Want to try again?"
                },
                'agreeing_to_try_again': {
                    "You're so strong-willed! I'm ready now.",
                    "I'm proud of you. Start when you're ready.",
                    "Go ahead.",
                    "I'm ready now.",
                    "Start when you're ready.",
                    "I'm ready when you are!"
                },
                'go_to_next_task': {
                    "Alright no problem. What exercise would you like?",
                    "Awh, too bad. That's okay though. What exercise would you like to do?",
                    "That's okay, you can always come back and try again. Tell me which exercise you want.",
                    "Alright. Which task do you want?"
                }
            }
        }
        
    # Function to return a sentence based on the state
    def generate(self, session_attributes, intent='default', word_info=None):
    
        # Set up local vars
        word = None
        task = None
    
        # Assign attributes to local vars
        state = session_attributes['state']['value']
        word = session_attributes['state']['word']
        if (state == 'attempt_task' or state == 'try_again') and intent == 'give_an_example_answer':
            task = session_attributes['state']['task']
            # Extend the name of the current task so it's understandable in a sentence
            # AND set intent to the task to add variety to possible responses
            if task == 'exa':
                task   = 'sentence'
                intent = 'exa'
            if task == 'def':
                task   = 'definition'
                intent = 'def'
            if task == 'syn':
                task   = 'synonym'
                intent = 'syn'
                
        # Only extend the name and assign the task
        if intent == 'specifying_a_task':
            task = session_attributes['state']['task']
            if task == 'exa':
                task   = 'sentence'
            if task == 'def':
                task   = 'definition'
            if task == 'syn':
                task   = 'synonym'
    
        # Get the response
        response = random.choice(list(self.data[state][intent]))
        
        # Substitute slots for their values 
        if not word == None:
            response = response.replace("[WORD]", word)
        if not task == None:
            response = response.replace("[TASK]", task)
        if not word_info == None:
            response = response.replace("[WORD_INFO]", word_info)
        
        return response
        
        
        
        
        
        
            