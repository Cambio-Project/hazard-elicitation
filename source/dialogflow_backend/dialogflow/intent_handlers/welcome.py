from typing import List, Dict

from dialogflow_backend.dialogflow.response_types import *
from dialogflow_backend.dialogflow.util import get_context, is_in_context
from util.text.text import text
from util.text.ids import *


async def welcome_handler(result) -> List[Dict]:
    conversation = []

    # Continue where the user last left.
    elicitation = get_context('c-elicitation', result)
    next_event = None
    if is_in_context('arch', elicitation):
        next_event = 'e-select-component'
        #conversation.append(ActionResponse.create('command', ['set-architecture', elicitation.parameters['arch']]))
    elif is_in_context('component', elicitation):
        next_event = 'e-specify-response'

    response = TextResponse.create(text(INTENT_WELCOME_TEXT))

    quick_reply = QuickReplyResponse()
    quick_reply.add_reply(text(INTENT_WELCOME_NO_TEXT), 'event', ['e-guide'])
    quick_reply.add_reply(text(INTENT_WELCOME_YES_TEXT), 'event', ['e-select-architecture'])
    # if next_event:
    #     quick_reply.add_reply(text(INTENT_WELCOME_RESUME_TEXT), 'event', [next_event])

    conversation.append(response)
    conversation.append(quick_reply.__repr__())

    return conversation


async def welcome_confirm_handler(result) -> List[Dict]:
    response = ActionResponse.create('command', ['event', 'e-select-architecture'])
    return [response]


async def welcome_decline_handler(result) -> List[Dict]:
    response = ActionResponse.create('command', ['event', 'e-guide'])
    return [response]
