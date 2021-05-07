from typing import List, Dict

from dialogflow_backend.dialogflow.response_types import *
from util.text.text import random_text, text
from util.text.ids import *


async def empty_handler(result) -> List[Dict]:
    return [EmptyResponse().__repr__()]


async def fallback_handler(result) -> List[Dict]:
    return [TextResponse.create(random_text(INTENT_FALLBACK_TEXT))]


async def bye_handler(result) -> List[Dict]:
    session_name = result.query_result.output_contexts[0].name
    session = session_name[session_name.find('sessions') + 9:session_name.rfind('/contexts')]

    return [
        TextResponse.create(random_text(INTENT_BYE_TEXT)),
        TextResponse.create(text(INTENT_BYE_QUESTIONNAIRE).format(session))
    ]


async def help_handler(result) -> List[Dict]:
    return [TextResponse.create(random_text(INTENT_HELP_TEXT)),
            ActionResponse.create('command', ['event', 'e-guide'])]
