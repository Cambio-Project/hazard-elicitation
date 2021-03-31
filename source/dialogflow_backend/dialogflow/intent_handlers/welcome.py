from typing import List, Dict

from dialogflow_backend.dialogflow.response_types import *
from dialogflow_backend.dialogflow.util import get_context, is_in_context, next_event
from util.text.text import text
from util.text.ids import *


async def welcome_handler(result) -> List[Dict]:
    conversation = [TextResponse.create(text(INTENT_WELCOME_TEXT))]

    quick_reply = QuickReplyResponse()
    quick_reply.add_reply(text(INTENT_WELCOME_NO_TEXT), 'event', ['e-guide'])
    quick_reply.add_reply(text(INTENT_WELCOME_YES_TEXT), 'event', ['e-select-architecture'])

    elicitation = get_context('c-elicitation', result)
    if is_in_context('arch', elicitation):
        arch = elicitation.parameters['arch']
        quick_reply.add_reply(text(INTENT_WELCOME_RESUME_TEXT), 'select-architecture', [arch])

    conversation.append(quick_reply.__repr__())

    return conversation


async def welcome_confirm_handler(result) -> List[Dict]:
    response = ActionResponse.create('command', ['event', 'e-select-architecture'])
    return [response]


async def welcome_decline_handler(result) -> List[Dict]:
    response = ActionResponse.create('command', ['event', 'e-guide'])
    return [response]


async def welcome_continue_handler(result) -> List[Dict]:
    elicitation = get_context('c-elicitation', result)
    if is_in_context('arch', elicitation):
        arch = elicitation.parameters['arch']

        return [ActionResponse.create('command', ['select-architecture', arch])]
    else:
        return [ActionResponse.create('command', ['event', 'e-select-architecture'])]
