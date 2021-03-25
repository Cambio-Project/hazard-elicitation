from typing import List, Dict

from dialogflow_backend.dialogflow.response_types import *
from util.text.text import random_text, text
from util.text.ids import *


async def empty_handler(result) -> List[Dict]:
    return [EmptyResponse().__repr__()]


async def fallback_handler(result) -> List[Dict]:
    return [TextResponse.create(random_text(INTENT_FALLBACK_TEXT))]


async def bye_handler(result) -> List[Dict]:
    return [TextResponse.create(random_text(INTENT_BYE_TEXT))]


async def help_handler(result) -> List[Dict]:
    return [TextResponse.create(random_text(INTENT_HELP_TEXT))]
