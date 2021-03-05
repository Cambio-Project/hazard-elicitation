from typing import List, Dict

from dialogflow_backend.dialogflow.response_types import *
from util.text.text import random_text, text
from util.text.ids import *


# Default handlers

async def empty_handler(result) -> List[Dict]:
    response = EmptyResponse()
    return [response.__repr__()]


async def fallback_handler(result) -> List[Dict]:
    response = TextMessage()
    response.text = random_text(INTENT_FALLBACK_TEXT)

    return [response.__repr__()]


async def help_handler(result) -> List[Dict]:
    response = TextMessage()
    response.text = random_text(INTENT_HELP_TEXT)
    return [response.__repr__()]
