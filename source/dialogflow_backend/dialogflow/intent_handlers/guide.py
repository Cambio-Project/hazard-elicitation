from typing import List, Dict

from dialogflow_backend.dialogflow.response_types import *
from dialogflow_backend.dialogflow.util import get_context, is_in_context, next_event
from util.text.text import random_text, text
from util.text.ids import *


async def guide_handler(result) -> List[Dict]:
    conversation = []

    # Add options to ask.
    quick_reply = QuickReplyResponse()
    for option in text(INTENT_GUIDE_OPTIONS):
        quick_reply.add_reply(option, 'event', ['e-guide', [{
            'name':       'c-guide-option',
            'lifespan':   1,
            'parameters': {'quick-option': option}
        }]])
    # Continue option
    quick_reply.add_reply(text(INTENT_GUIDE_CONTINUE_CONFIRM_TEXT), 'event', [next_event(result)])

    # Check if option is given by the user.
    option_context = get_context('c-guide-option', result)
    if is_in_context('quick-option', option_context):
        option_value = option_context.parameters['quick-option']
    elif is_in_context('option', result.query_result):
        option_value = result.query_result.parameters['option']
    else:
        option_value = None

    conversation.append(FormattingResponse.create('divider'))

    # If option is given, explain it and add further quick reply options.
    if option_value:
        conversation.append(CardResponse.create(option_value, **text(INTENT_GUIDE_OPTIONS)[option_value]))
        conversation.append(TextResponse.create(random_text(INTENT_GUIDE_CONTINUE_TEXT)))

    # Otherwise tell the user to ask something.
    else:
        conversation.append(TextResponse.create(text(INTENT_GUIDE_TEXT)))

    conversation.append(quick_reply.__repr__())

    return conversation


async def guide_option_handler(result) -> List[Dict]:
    return await guide_handler(result)


async def guide_confirm_handler(result) -> List[Dict]:
    response = ActionResponse.create('command', ['event', next_event(result)])
    return [response]
