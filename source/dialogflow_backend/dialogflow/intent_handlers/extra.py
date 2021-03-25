from random import randint
from typing import List, Dict

import requests
import json

from dialogflow_backend.dialogflow.response_types import *
from util.log import debug
from util.text.text import random_text
from util.text.ids import *


# Extra handlers

async def fact_handler(result) -> List[Dict]:
    random = 'http://numbersapi.com/random/trivia'
    data = requests.get(random)

    fact = CardResponse()
    fact.title = 'Fact from numbersapi.com'
    fact.text = data.text

    if randint(0, 10) < 6:
        return [fact.__repr__(), TextResponse.create(random_text(INTENT_FACT_TEXT))]

    return [fact.__repr__()]


async def joke_handler(result) -> List[Dict]:
    no_response = False
    try:
        if randint(0, 10) < 5:
            url = 'https://official-joke-api.appspot.com/random_joke'
            data = json.loads(requests.get(url).text or {})
        else:
            url = 'https://official-joke-api.appspot.com/jokes/programming/random'
            data = json.loads(requests.get(url).text[0] or {})

    except BaseException as e:
        debug(e)
        no_response = True
        data = {'setup': 'We are out of jokes...', 'punchline': '...please try later'}

    joke = AccordionResponse()
    joke.add_pane(data['setup'], data['punchline'])

    if not no_response and randint(0, 10) < 6:
        return [joke.__repr__(), TextResponse.create(random_text(INTENT_JOKE_TEXT))]

    return [joke.__repr__()]
