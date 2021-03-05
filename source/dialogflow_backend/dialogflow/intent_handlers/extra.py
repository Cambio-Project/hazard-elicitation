from random import randint
from typing import List, Dict

import requests
import json

from dialogflow_backend.dialogflow.response_types import *
from util.text.text import random_text
from util.text.ids import *


# Extra handlers

async def fact_handler(result) -> List[Dict]:
    random = 'http://numbersapi.com/random/trivia'
    data = requests.get(random)

    fact = Card()
    fact.title = 'Fact from numbersapi.com'
    fact.text = data.text

    if randint(0, 10) < 6:
        response = TextMessage()
        response.text = random_text(INTENT_FACT_TEXT)

        return [fact.__repr__(), response.__repr__()]

    return [fact.__repr__()]


async def joke_handler(result) -> List[Dict]:
    if randint(0, 10) < 5:
        url = 'https://official-joke-api.appspot.com/random_joke'
        data = json.loads(requests.get(url).text)
    else:
        url = 'https://official-joke-api.appspot.com/jokes/programming/random'
        data = json.loads(requests.get(url).text[0])

    joke = Accordion()
    joke.add_pane(data['setup'], data['punchline'])

    if randint(0, 10) < 6:
        response = TextMessage()
        response.text = random_text(INTENT_JOKE_TEXT)

        return [joke.__repr__(), response.__repr__()]

    return [joke.__repr__()]
