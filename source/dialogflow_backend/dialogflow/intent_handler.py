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
    response.text = random_text(INTENT_FALLBACK_TEXT)

    return [response.__repr__()]


async def help_handler(result) -> List[Dict]:
    response = TextMessage()
    response.text = random_text(INTENT_HELP_TEXT)
    return [response.__repr__()]


async def guide_handler(result) -> List[Dict]:
    context = await get_context('c-guide-option', result)
    conversation = []

    quick_reply = QuickReply()

    for option in text(INTENT_GUIDE_OPTIONS):
        quick_reply.add_reply(option, 'event', ['e-guide', [{
            'name':       'c-guide-option',
            'lifespan':   1,
            'parameters': {
                'option': option
            },
        }]])
    quick_reply.add_reply('I am good, let\'s continue! &#x2714;', 'event', ['e-select-architecture'])

    if context and 'option' in context.parameters:
        divider = FormattingMessage()
        divider.text = 'divider'

        response = TextMessage()
        response.text = text(INTENT_GUIDE_OPTIONS)[context.parameters['option']]

        more = TextMessage()
        more.text = random_text(INTENT_GUIDE_CONTINUE)

        conversation.append(divider.__repr__())
        conversation.append(response.__repr__())
        conversation.append(more.__repr__())
        conversation.append(quick_reply.__repr__())

    else:
        response = TextMessage()
        response.text = text(INTENT_GUIDE_TEXT)

        conversation.append(response.__repr__())
        conversation.append(quick_reply.__repr__())

    return conversation


async def guide_option_handler(result) -> List[Dict]:
    response = ActionResponse()
    response.action = 'command'
    response.values = ['event', 'e-guide', [{
        'name':       'e-guide-option',
        'lifespan':   1,
        'parameters': {
            'option': result.query_result.parameters['option']
        }
    }]]
    return [response.__repr__()]


async def guide_confirm_handler(result) -> List[Dict]:
    response = ActionResponse()
    response.action = 'command'
    response.values = ['event', 'e-select-architecture']
    return [response.__repr__()]


# Welcome

async def welcome_handler(result) -> List[Dict]:
    response = TextMessage()
    response.text = text(INTENT_WELCOME_TEXT)

    quick_reply = QuickReply()
    quick_reply.add_reply(text(INTENT_WELCOME_NO_TEXT), 'event', ['e-guide'])
    quick_reply.add_reply(text(INTENT_WELCOME_YES_TEXT), 'event', ['e-select-architecture'])
    return [response.__repr__(), quick_reply.__repr__()]


async def welcome_confirm_handler(result) -> List[Dict]:
    response = ActionResponse()
    response.action = 'command'
    response.values = ['event', 'e-select-architecture']
    return [response.__repr__()]


async def welcome_decline_handler(result) -> List[Dict]:
    response = ActionResponse()
    response.action = 'command'
    response.values = ['event', 'e-guide']
    return [response.__repr__()]


# Elicitation handlers

async def elicitation_select_architecture_handler(result) -> List[Dict]:
    divider = FormattingMessage()
    divider.text = 'divider'

    question = TextMessage()
    question.text = text(INTENT_ELICITATION_SELECT_ARCHITECTURE_TEXT)

    architectures = []

    def c():
        for a in ArchitectureModel.objects.all():
            architectures.append(a.name)

    await sync_to_async(c)()

    quick_replies = QuickReply()
    for arch in architectures:
        quick_replies.add_reply(arch, 'select-architecture', [arch])

    return [
        divider.__repr__(),
        question.__repr__(),
        quick_replies.__repr__()]


async def elicitation_select_component_handler(result) -> List[Dict]:
    context = await get_context('c-elicitation', result)

    divider = FormattingMessage()
    divider.text = 'divider'

    response = TextMessage()
    response.text = text(INTENT_ELICITATION_SELECT_COMPONENT_TEXT).format(context.parameters['arch'])

    services = TextMessage()
    services.text = text(INTENT_ELICITATION_SELECT_COMPONENT_SERVICE_TEXT)
    service_replies = QuickReply()

    operations = TextMessage()
    operations.text = text(INTENT_ELICITATION_SELECT_COMPONENT_OPERATION_TEXT)
    operation_replies = QuickReply()

    context = await get_context('c-graph', result)

    if context:
        nodes = context.parameters['arch']['nodes']
        for node in nodes:
            service_replies.add_reply(node, 'select-element', ['node', node, ''])

        edges = context.parameters['arch']['edges']
        for edge in edges:
            operation_replies.add_reply(edge, 'select-element', ['edge', edge, ''])

    return [
        divider.__repr__(),
        response.__repr__(),
        services.__repr__(),
        service_replies.__repr__(),
        operations.__repr__(),
        operation_replies.__repr__(),
    ]


async def elicitation_specify_response(result) -> List[Dict]:
    context = await get_context('c-elicitation', result)

    if False:
        pass

    if context and 'component' in context.parameters:
        divider = FormattingMessage()
        divider.text = 'divider'

        response = TextMessage()
        response.text = text(INTENT_ELICITATION_SPECIFY_RESPONSE_TEXT).format(context.parameters['component'])

        return [
            divider.__repr__(),
            response.__repr__()
        ]
    else:
        response = ActionResponse()
        response.action = 'command'
        response.values = ['event', 'e-select-component']
        return [response.__repr__()]


# Config handlers

async def config_handler(result) -> List[Dict]:
    response = ActionResponse()
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
    response.add_pane('Commands', cmd_list)
    return [response.__repr__()]


async def manage_handler(result) -> List[Dict]:
    response = ActionResponse()
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
