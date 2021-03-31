from typing import List, Dict

from dialogflow_backend.dialogflow.intent_handlers.elicitation.stimulus import elicitation_stimuli_handler
from dialogflow_backend.dialogflow.response_types import ActionResponse, FormattingResponse, CardResponse, \
    QuickReplyResponse
from dialogflow_backend.dialogflow.util import get_context, is_in_context, set_context_parameters
from util.log import error
from util.text.ids import INTENT_ELICITATION_RESPONSE_TEXT, STIMULUS_RESPONSE_TEXTS
from util.text.text import text, random_selection


async def elicitation_response_handler(result) -> List[Dict]:
    try:
        conversation = []

        elicitation = get_context('c-elicitation', result)
        config_context = get_context('c-config', result)

        # Response was given as text.
        if is_in_context('response', config_context):
            return [ActionResponse.create('command', ['event', 'e-specify-response-measure', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'response': config_context.parameters['response']
                }
            }]])]

        # Provide the user with response options
        conversation.append(FormattingResponse.create('divider'))

        content = text(INTENT_ELICITATION_RESPONSE_TEXT)
        response = CardResponse.create(
            title=content['title'].format(elicitation.parameters['component']),
            text=content['text'])
        conversation.append(response)

        responses = text(STIMULUS_RESPONSE_TEXTS)[elicitation.parameters['artifact']]['responses']

        quick_reply = QuickReplyResponse()
        for option in responses:
            quick_reply.add_reply(option, 'event', ['e-specify-response-measure', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'response': option
                }}]])
        conversation.append(quick_reply.__repr__())

        return conversation

    except Exception as e:
        error(e)
        return await elicitation_stimuli_handler(result)


async def elicitation_response_followup_handler(result) -> List[Dict]:
    return await elicitation_response_handler(result)


async def elicitation_response_default_handler(result) -> List[Dict]:
    elicitation = get_context('c-elicitation', result)
    if elicitation:
        responses = text(STIMULUS_RESPONSE_TEXTS)[elicitation.parameters['artifact']]['responses']
        result = set_context_parameters(result, 'c-config', {'response': random_selection(responses)})
    return await elicitation_response_handler(result)
