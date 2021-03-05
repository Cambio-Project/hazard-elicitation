from typing import List, Dict

from dialogflow_backend.dialogflow.response_types import *
from dialogflow_backend.dialogflow.util import get_context
from util.text.text import random_text, text
from util.text.ids import *


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
