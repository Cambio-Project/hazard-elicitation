from typing import List, Dict

from google.protobuf.struct_pb2 import ListValue

from dialogflow_backend.dialogflow.intent_handlers.elicitation.response import elicitation_response_handler
from dialogflow_backend.dialogflow.response_types import FormattingResponse, ActionResponse, QuickReplyResponse, \
    CardResponse
from dialogflow_backend.dialogflow.util import get_context, is_in_context, set_context_parameters
from util.log import error
from util.text.ids import INTENT_ELICITATION_DESCRIPTION_QUICK_RESPONSE, INTENT_ELICITATION_DESCRIPTION_TEXT
from util.text.text import text


async def elicitation_description_handler(result) -> List[Dict]:
    try:
        conversation = [FormattingResponse.create('divider')]
        elicitation = get_context('c-elicitation', result)
        config_context = get_context('c-config', result)

        if is_in_context('description', config_context):
            description = config_context.parameters['description']
            if isinstance(description, (list, ListValue)):
                description = ' '.join(config_context.parameters['description'])
            else:
                description = config_context.parameters['description']

            return [ActionResponse.create('command', ['event', 'e-save-scenario', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'description': description
                }
            }]])]

        quick_response_text = text(INTENT_ELICITATION_DESCRIPTION_QUICK_RESPONSE).format(
            elicitation.parameters['stimulus'],
            elicitation.parameters['artifact'].lower(),
            elicitation.parameters['component'])

        quick_response = QuickReplyResponse()
        quick_response.add_reply(quick_response_text, 'event', ['e-save-scenario', [{
            'name':       'c-elicitation',
            'lifespan':   100,
            'parameters': {
                'description': quick_response_text
            }
        }]])

        conversation.append(CardResponse.create(**text(INTENT_ELICITATION_DESCRIPTION_TEXT)))
        conversation.append(quick_response.__repr__())
        return conversation

    except Exception as e:
        error(e)
        return await elicitation_response_handler(result)


async def elicitation_description_followup_handler(result) -> List[Dict]:
    return await elicitation_description_handler(result)


async def elicitation_description_default_handler(result) -> List[Dict]:
    elicitation = get_context('c-elicitation', result)
    if elicitation:
        description = text(INTENT_ELICITATION_DESCRIPTION_QUICK_RESPONSE).format(
            elicitation.parameters['stimulus'],
            elicitation.parameters['artifact'].lower(),
            elicitation.parameters['component'])
        result = set_context_parameters(result, 'c-config', {'description': description})

    return await elicitation_description_handler(result)
