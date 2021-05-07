from random import randint, choice
from typing import List, Dict

from dialogflow_backend.dialogflow.intent_handlers.elicitation.architecture import elicitation_architecture_handler
from dialogflow_backend.dialogflow.response_types import ActionResponse, TextResponse, FormattingResponse, CardResponse, \
    QuickReplyResponse
from dialogflow_backend.dialogflow.util import get_context, is_in_context, set_context_parameters
from util.log import error
from util.text.ids import INTENT_ELICITATION_COMPONENT_MISSING_TEXT, INTENT_ELICITATION_COMPONENT_TEXT, \
    INTENT_ELICITATION_COMPONENT_SERVICE_TEXT, INTENT_ELICITATION_COMPONENT_OPERATION_TEXT
from util.text.text import text


async def get_nodes(nodes):
    nodes = {k: v[1] for k, v in sorted(nodes.items())}
    return {k: v for k, v in sorted(nodes.items(), key=lambda o: o[1], reverse=True)}


async def get_edges(edges):
    edges = {k: v[1] for k, v in sorted(edges.items())}
    return {k: v for k, v in sorted(edges.items(), key=lambda o: o[1], reverse=True)}


async def elicitation_component_handler(result) -> List[Dict]:
    try:
        conversation = []

        elicitation = get_context('c-elicitation', result)
        graph_context = get_context('c-graph', result)
        config_context = get_context('c-config', result)

        # Component name was given as text.
        if is_in_context('component-name', config_context):
            component_type = config_context.parameters['component-type']
            component_name = config_context.parameters['component-name']

            # Check against available operations.
            if component_type == 'operation' or component_name in graph_context.parameters['arch']['edges']:
                return [ActionResponse.create('command', ['select-element', 'edge', component_name])]

            # Check against available services.
            elif component_type == 'service' or component_name in graph_context.parameters['arch']['nodes']:
                return [ActionResponse.create('command', ['select-element', 'node', component_name])]

            # Prompt the user to try again.
            missing = text(INTENT_ELICITATION_COMPONENT_MISSING_TEXT)
            return [TextResponse.create(missing.format(component_type, component_name))]

        # Provide the user with a selection of services and operations.
        conversation.append(FormattingResponse.create('divider'))
        content = text(INTENT_ELICITATION_COMPONENT_TEXT)
        response = CardResponse.create(title=content['title'].format(elicitation.parameters['arch']),
                                       text=content['text'], spoiler=content['spoiler'])
        conversation.append(response)

        # Services
        services = TextResponse.create(text(INTENT_ELICITATION_COMPONENT_SERVICE_TEXT))
        service_replies = QuickReplyResponse()

        nodes = await get_nodes(graph_context.parameters['arch']['nodes'])
        for i, node in enumerate(nodes):
            if i == 5:
                break
            service_replies.add_reply(node, 'select-element', ['node', node])

        conversation.append(services)
        conversation.append(service_replies.__repr__())

        # Operations
        operations = TextResponse.create(text(INTENT_ELICITATION_COMPONENT_OPERATION_TEXT))
        operation_replies = QuickReplyResponse()

        edges = await get_edges(graph_context.parameters['arch']['edges'])
        for i, edge in enumerate(edges):
            if i == 5:
                break
            operation_replies.add_reply(edge, 'select-element', ['edge', edge])

        conversation.append(operations)
        conversation.append(operation_replies.__repr__())

        return conversation

    except Exception as e:
        error(e)
        return await elicitation_architecture_handler(result)


async def elicitation_component_followup_handler(result) -> List[Dict]:
    return await elicitation_component_handler(result)


async def elicitation_component_default_handler(result) -> List[Dict]:
    graph_context = get_context('c-graph', result)
    if graph_context:
        if not randint(0, 10) < 6:
            edges = await get_edges(graph_context.parameters['arch']['edges'])
            name = choice(list(edges.keys()))
            result = set_context_parameters(result, 'c-config', {'component-name': name, 'component-type': 'operation'})
        else:
            nodes = await get_nodes(graph_context.parameters['arch']['nodes'])
            name = choice(list(nodes.keys()))
            result = set_context_parameters(result, 'c-config', {'component-name': name, 'component-type': 'service'})

    return await elicitation_component_handler(result)
