from typing import List, Dict

from dialogflow_backend.dialogflow.response_types import *
from util.text.text import text
from util.text.ids import *

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

