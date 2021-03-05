from typing import List, Dict

from asgiref.sync import sync_to_async

from architecture_extraction_backend.models import ArchitectureModel
from dialogflow_backend.dialogflow.response_types import *
from dialogflow_backend.dialogflow.util import get_context
from util.text.text import text
from util.text.ids import *


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
