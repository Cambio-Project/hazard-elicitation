from random import randint
from typing import List, Dict

import requests
import json

from asgiref.sync import sync_to_async

from architecture_extraction_backend.models import ArchitectureModel
from dialogflow_backend.dialogflow.settings import COMMANDS
from dialogflow_backend.dialogflow.response_types import *
from util.text.text import random_text, text
from util.text.ids import *


# Helper functions

async def get_context(name, result):
    for context in result.query_result.output_contexts:
        context_name = context.name[context.name.rfind('/') + 1:]
        if context_name == name:
            return context
    return None


# Default handlers

async def empty_handler(result) -> List[Dict]:
    response = EmptyResponse()
    return [response.__repr__()]


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
    intent = text(INTENT_WELCOME_NAME)

    response = TextMessage()
    response.intent = intent
    response.text = text(INTENT_WELCOME_TEXT)

    quick_reply = QuickReply()
    quick_reply.intent = intent
    quick_reply.add_reply('Yes, let\'s go! &#x1F44D;', 'event', ['select-architecture'])
    return [response.__repr__(), quick_reply.__repr__()]


# Elicitation handlers

async def elicitation_select_architecture_handler(result) -> List[Dict]:
    intent = text(INTENT_ELICITATION_SELECT_ARCHITECTURE_NAME)

    question = TextMessage()
    question.intent = intent
    question.text = text(INTENT_ELICITATION_SELECT_ARCHITECTURE_TEXT)

    architectures = []

    def c():
        for a in ArchitectureModel.objects.all():
            architectures.append(a.name)

    await sync_to_async(c)()

    quick_replies = QuickReply()
    quick_replies.intent = intent
    for arch in architectures:
        quick_replies.add_reply(arch, 'select-architecture', [arch])

    return [question.__repr__(), quick_replies.__repr__()]


async def elicitation_select_component_handler(result) -> List[Dict]:
    intent = text(INTENT_ELICITATION_SELECT_COMPONENT_NAME)

    context = await get_context('elicitation', result)

    divider = FormattingMessage()
    divider.text = 'divider'

    response = TextMessage()
    response.intent = intent
    response.text = text(INTENT_ELICITATION_SELECT_COMPONENT_TEXT).format(context.parameters['arch'])

    services = TextMessage()
    services.text = text(INTENT_ELICITATION_SELECT_COMPONENT_TEXT_SERVICE)
    service_replies = QuickReply()

    operations = TextMessage()
    operations.text = text(INTENT_ELICITATION_SELECT_COMPONENT_TEXT_OPERATION)
    operation_replies = QuickReply()

    context = await get_context('graph', result)

    if context:
        nodes = context.parameters['arch']['nodes']
        for node in nodes:
            service_replies.add_reply(node, 'select-element', ['node', node, ""])

        edges = context.parameters['arch']['edges']
        for edge in edges:
            operation_replies.add_reply(edge, 'select-element', ['edge', edge, ""])

    return [
        divider.__repr__(),
        response.__repr__(),
        services.__repr__(),
        service_replies.__repr__(),
        operations.__repr__(),
        operation_replies.__repr__(),
        divider.__repr__()]


async def elicitation_specify_response(result) -> List[Dict]:
    intent = text(INTENT_ELICITATION_SPECIFY_RESPONSE_NAME)

    context = await get_context('elicitation', result)
    print(context.parameters)

    response = TextMessage()
    response.intent = intent
    response.text = text(INTENT_ELICITATION_SPECIFY_RESPONSE_TEXT).format(context.parameters['component'])

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


# Config handlers

async def config_handler(result) -> List[Dict]:
    response = ActionResponse()
    response.intent = text(INTENT_COMMAND_CONFIG_NAME)
    response.action = 'command'
    response.values = [
        result.query_result.parameters['config-command'],
        result.query_result.parameters['config-command-value']
    ]
    return [response.__repr__()]


async def config_list_handler(result) -> List[Dict]:
    def code_list(e): return '<{0}><{1}>{2}</{1}></{0}>'.format('li', 'code', e)

    cmd_list = '<ul>{}</ul>'.format(''.join(map(code_list, COMMANDS.keys())))

    response = Accordion()
    response.intent = text(INTENT_COMMAND_CONFIG_LIST_NAME)
    response.add_pane('Commands', cmd_list)
    return [response.__repr__()]


async def manage_handler(result) -> List[Dict]:
    response = ActionResponse()
    response.intent = text(INTENT_COMMAND_CONFIG_NAME)
    response.action = 'command'
    response.values = [
        result.query_result.parameters['manage-command'],
        result.query_result.parameters['manage-command-property'],
        result.query_result.parameters['manage-command-value']
    ]
    return [response.__repr__()]


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
    random = 'https://official-joke-api.appspot.com/random_joke'
    # programming = 'https://official-joke-api.appspot.com/jokes/programming/random'

    data = json.loads(requests.get(random).text)

    joke = Accordion()
    joke.add_pane(data['setup'], data['punchline'])

    if randint(0, 10) < 6:
        response = TextMessage()
        response.text = random_text(INTENT_JOKE_TEXT)

        return [joke.__repr__(), response.__repr__()]

    return [joke.__repr__()]
