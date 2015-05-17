# -*- coding: utf-8-*-
import random
import re
from client import jasperpath

WORDS = ["HELLO", 
         "HI", 
         "HOW ARE YOU", 
         "HOW'RE YOU", 
         "HOW ARE THINGS", 
         "HOW'RE THINGS", 
         "WHAT'S UP", 
         "WHAT IS UP", 
         "WHAT'S HAPPENING", 
         "WHAT YOU DOING", 
         "WHAT ARE YOU DOING", 
         "WHAT'RE YOU DOING"]

PRIORITY = 1


def handle(text, mic, profile):
    """
        Responds to the message Hello or Hi with a random response.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    if re.search(r'\b(how are you|how\'re you|how are things|how\'re things)\b', text, re.IGNORECASE):
        responses = ["Doing good thanks", 
                     "All good here", 
                     "Not bad thanks how are you %s" % profile['first_name'], 
                     "Do you really care?"]
    elif re.search(r'\b(what\'s up|what is up|what\'s happening)\b', text, re.IGNORECASE):
        responses = ["Not much, you?", 
                     "Just sitting here, chilling"]
    elif re.search(r'\b(what are you doing|what\'re you doing|what you doing)\b', text, re.IGNORECASE):
        responses = ["Solving the world's problems",
                     "I've got 99 problems but this ain't one",
                     "Talking to you %s" % profile['first_name']]
    else:
        responses = ["Hello", 
                     "Hi there", 
                     "Hey there", 
                     "What's up"]

    mic.say(random.choice(responses))


def isValid(text):
    """
        Returns True if the input is related to jokes/humor.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(hello|hi|how are you|how\'re you|how are things|how\'re things|what\'s up|what is up|what\'s happening|what you doing|what are you doing|what\'re you doing)\b', text, re.IGNORECASE))
