from typing import List, Dict

import requests
import json

from dialogflow_backend.dialogflow.commands import COMMANDS
from dialogflow_backend.dialogflow.responses import TextMessage, QuickReply, Card, Accordion, ActionResponse
from util.text.text import random_text, text
from util.text.ids import *


async def fallback_handler(result) -> List[Dict]:
    response = TextMessage()
    response.intent = text(INTENT_FALLBACK_NAME)
    response.text = random_text(INTENT_FALLBACK_TEXT)

    return [response.__repr__()]


async def help_handler(result) -> List[Dict]:
    response = TextMessage()
    response.intent = text(INTENT_HELP_NAME)
    response.text = random_text(INTENT_HELP_TEXT)
    return [response.__repr__()]


async def welcome_handler(result) -> List[Dict]:
    response = TextMessage()
    response.intent = text(INTENT_WELCOME_NAME)
    response.text = random_text(INTENT_WELCOME_TEXT)
    return [response.__repr__()]


async def elicitation_question_handler(result) -> List[Dict]:
    intent = text(INTENT_ELICITATION_QUESTION_NAME)

    question = TextMessage()
    question.intent = intent
    question.text = random_text(INTENT_ELICITATION_QUESTION_TEXT)

    quick_replies = QuickReply()
    quick_replies.intent = intent
    quick_replies.add_reply('Yes', '', [])
    quick_replies.add_reply('No', '', [])
    return [question.__repr__(), quick_replies.__repr__()]


async def config_handler(result) -> List[Dict]:
    response = ActionResponse()
    response.intent = text(INTENT_CONFIG_COMMAND_NAME)
    response.action = 'command'
    response.values = [result.query_result.parameters['command'], 'bool', result.query_result.parameters['value']]
    return [response.__repr__()]


async def config_list_handler(result) -> List[Dict]:
    def code_list(e): return '<{0}><{1}>{2}</{1}></{0}>'.format('li', 'code', e)
    cmd_list = '<ul>{}</ul>'.format(''.join(map(code_list, COMMANDS.keys())))

    response = Accordion()
    response.intent = text(INTENT_CONFIG_COMMAND_LIST_NAME)
    response.add_pane('Commands', cmd_list)
    return [response.__repr__()]


async def fact_handler(result) -> List[Dict]:
    random = 'http://numbersapi.com/random/trivia'
    data = requests.get(random)

    fact = Card()
    fact.title = 'Fact from numbersapi.com'
    fact.text = data.text
    return [fact.__repr__()]


async def joke_handler(result) -> List[Dict]:
    random = 'https://official-joke-api.appspot.com/random_joke'
    # programming = 'https://official-joke-api.appspot.com/jokes/programming/random'

    data = json.loads(requests.get(random).text)

    joke = Accordion()
    joke.add_pane(data['setup'], data['punchline'])
    return [joke.__repr__()]
