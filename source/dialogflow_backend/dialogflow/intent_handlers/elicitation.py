from typing import List, Dict

from asgiref.sync import sync_to_async

from architecture_extraction_backend.models import ArchitectureModel
from dialogflow_backend.dialogflow.response_types import *
from dialogflow_backend.dialogflow.util import get_context, is_in_context
from util.text.text import text
from util.text.ids import *


# Elicitation handlers

async def elicitation_select_architecture_handler(result) -> List[Dict]:
    divider = FormattingResponse.create('divider')
    content = text(INTENT_ELICITATION_SELECT_ARCHITECTURE_TEXT)
    question = CardResponse.create(title=content['title'], text=content['text'])

    architectures = []

    def c():
        for a in ArchitectureModel.objects.all():
            architectures.append(a.name)

    await sync_to_async(c)()

    quick_replies = QuickReplyResponse()
    for arch in architectures:
        quick_replies.add_reply(arch, 'select-architecture', [arch])

    return [divider, question, quick_replies.__repr__()]


async def elicitation_select_component_handler(result) -> List[Dict]:
    conversation = []

    elicitation = get_context('c-elicitation', result)
    graph_context = get_context('c-graph', result)

    # Text
    conversation.append(FormattingResponse.create('divider'))

    content = text(INTENT_ELICITATION_SELECT_COMPONENT_TEXT)
    response = CardResponse.create(
        title=content['title'].format(elicitation.parameters['arch']),
        text=content['text'])

    conversation.append(response)

    # Services
    services = TextResponse.create(text(INTENT_ELICITATION_SELECT_COMPONENT_SERVICE_TEXT))
    service_replies = QuickReplyResponse()

    nodes = graph_context.parameters['arch']['nodes']
    for node in nodes:
        service_replies.add_reply(node, 'select-element', ['node', node, ''])

    conversation.append(services)
    conversation.append(service_replies.__repr__())

    # Operations
    operations = TextResponse.create(text(INTENT_ELICITATION_SELECT_COMPONENT_OPERATION_TEXT))
    operation_replies = QuickReplyResponse()

    edges = graph_context.parameters['arch']['edges']
    for edge in edges:
        operation_replies.add_reply(edge, 'select-element', ['edge', edge, ''])

    conversation.append(operations)
    conversation.append(operation_replies.__repr__())

    return conversation


async def elicitation_specify_response_handler(result) -> List[Dict]:
    context = get_context('c-elicitation', result)

    if is_in_context('component', context):
        conversation = [FormattingResponse.create('divider')]

        content = text(INTENT_ELICITATION_SPECIFY_RESPONSE_TEXT)
        response = CardResponse.create(
            title=content['title'].format(context.parameters['component']),
            text=content['text'])
        conversation.append(response)

        conversation.append(TextResponse.create())

        return conversation

    else:
        return await elicitation_select_component_handler(result)


async def elicitation_specify_response_measure_handler(result) -> List[Dict]:
    context = get_context('c-elicitation', result)

    if is_in_context('response', context):
        conversation = [FormattingResponse.create('divider')]

        content = text(INTENT_ELICITATION_SPECIFY_RESPONSE_MEASURE_TEXT)
        response = CardResponse.create(
            title=content['title'].format(context.parameters['component']),
            text=content['text'])
        conversation.append(response)

        return conversation

    else:
        return await elicitation_specify_response_handler(result)


async def elicitation_save_scenario_handler(result) -> List[Dict]:
    context = get_context('c-elicitation', result)

    if is_in_context('response_measure', context):
        conversation = [FormattingResponse.create('divider')]

        content = text(INTENT_ELICITATION_SAVE_SCENARIO_TEXT)
        response = CardResponse.create(title=content['title'], text=content['text'])
        conversation.append(response)

        parameters = AccordionResponse.create([
            {'title': 'Architecture', 'text': ''},
            {'title': 'Component', 'text': ''},
            {'title': 'Response', 'text': ''},
            {'title': 'Response Measure', 'text': ''}
        ])
        conversation.append(parameters)

        return conversation

    else:
        return await elicitation_specify_response_measure_handler(result)
