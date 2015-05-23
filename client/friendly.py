# -*- coding: utf-8-*-
import random

def hello(mic, profile):
    """
    Says hello
    """

    responses = [
        "Hey %s" % profile['first_name'],
        "Hi there %s" % profile['first_name'],
        "What's up %s" % profile['first_name'],
        "Yo %s" % profile['first_name']
    ]

    mic.say(random.choice(responses))


def goodbye(mic, profile):
    """
    Says goodbye
    """

    responses = [
        "See ya %s" % profile['first_name'],
        "Chow %s" % profile['first_name']
    ]

    mic.say(random.choice(responses))


def thinking(mic, profile):
    """
    Returns a random phrase indicating that we're thinking about something
    """

    responses = [
        "Let me look that up",
        "Let me think",
        "Okay, give me a second",
        "That's an easy one",
        "Ooh, I know this one"
    ]

    mic.say(random.choice(responses))


