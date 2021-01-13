from typing import List, Dict

import requests
import json

from util.text.text import random_text
from util.text.ids import *


async def fallback_handler() -> List[Dict]:
    return [{
        'type':    'text',
        'payload': random_text(INTENT_FALLBACK_TEXT)
    }]


async def fallback_gibberish_handler() -> List[Dict]:
    return [{
        'type':    'text',
        'payload': random_text(INTENT_FALLBACK_GIBBERISH_TEXT)
    }]


async def fallback_insult_handler() -> List[Dict]:
    return [{
        'type':    'text',
        'payload': random_text(INTENT_FALLBACK_INSULT_TEXT)
    }]


async def help_handler() -> List[Dict]:
    return [{
        'type':    'text',
        'payload': random_text(INTENT_HELP_TEXT)
    }]


async def welcome_handler() -> List[Dict]:
    return [{
        'type':    'text',
        'payload': random_text(INTENT_WELCOME_TEXT)
    }]


async def elicitation_question_handler() -> List[Dict]:
    return [{
        'type':    'text',
        'payload': random_text(INTENT_ELICITATION_QUESTION_TEXT)
    }, {
        'type':    'quick_reply',
        'payload': ['Yes', 'No']
    }]


async def fact_handler() -> List[Dict]:
    random = 'http://numbersapi.com/random/trivia'
    data = requests.get(random)
    fact = data.text

    return [{
        'type':    'card',
        'payload': {
            'title':   'Fact from numbersapi.com',
            'message': fact}
    }]


async def joke_handler() -> List[Dict]:
    random = 'https://official-joke-api.appspot.com/random_joke'
    programming = 'https://official-joke-api.appspot.com/jokes/programming/random'

    data = requests.get(random)
    joke = json.loads(data.text)

    return [{
        'type':    'accordion',
        'payload': [
            {
                'title':   joke['setup'],
                'content': joke['punchline']}
        ]
    }]
