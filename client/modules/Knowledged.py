# -*- coding: utf-8-*-
import random
import re
import wolframalpha
import time
import sys
import string
from sys import maxint
from client import friendly, jasperpath

WORDS = ["WHO", "WHAT", "HOW MUCH", "HOW MANY", "HOW OLD"]


def handle(text, mic, profile):
    app_id = profile['keys']['WOLFRAMALPHA']
    client = wolframalpha.Client(app_id)

    friendly.thinking(mic, profile)

    query = client.query(text)

    if len(query.pods) > 0:
        texts = ""
        pod = query.pods[1]
        if pod.text:
            texts = pod.text
            texts = filter(lambda x: x in string.printable, texts)
        else:
            texts = "I can not find anything"

        lines = texts.split("\n")
        for line in lines:
            mic.say(line.replace("|",""))
    else:
        mic.say("Sorry, Could you be more specific?.")




def isValid(text):
    if re.search(r'\bwho\b', text, re.IGNORECASE):
        return True
    elif re.search(r'\bwhat\b', text, re.IGNORECASE):
        return True
    elif re.search(r'\bhow much\b', text, re.IGNORECASE):
        return True
    elif re.search(r'\bhow MANY\b', text, re.IGNORECASE):
        return True
    elif re.search(r'\bhow old\b', text, re.IGNORECASE):
        return True
    else:
        return False
