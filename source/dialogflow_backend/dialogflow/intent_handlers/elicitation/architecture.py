from typing import List, Dict

from asgiref.sync import sync_to_async

from software_architecture_extraction.source.extractor.models.architecture import ArchitectureModel
from dialogflow_backend.dialogflow.response_types import ActionResponse, TextResponse, FormattingResponse, CardResponse, \
    QuickReplyResponse
from dialogflow_backend.dialogflow.util import get_context, is_in_context, set_context_parameters
from util.text.ids import INTENT_ELICITATION_ARCHITECTURE_TEXT
from util.text.text import text, random_selection


def fetch_architectures(collection):
    for a in ArchitectureModel.objects.all():
        collection.append(a.name)


async def elicitation_architecture_handler(result) -> List[Dict]:
    architectures = []
    await sync_to_async(fetch_architectures)(architectures)

    # Architecture was given as text
    config_context = get_context('c-config', result)
    if is_in_context('arch-file', config_context):

        arch_name = config_context.parameters['arch-file']
        if arch_name in architectures:
            # If architecture name exists, select the matching one.
            return [ActionResponse.create('command', ['select-architecture', arch_name])]

        # Prompt the user to try again.
        return [TextResponse.create('Try again')]

    # Give the user a selection of available architectures.
    divider = FormattingResponse.create('divider')
    content = text(INTENT_ELICITATION_ARCHITECTURE_TEXT)
    question = CardResponse.create(title=content['title'], text=content['text'])

    quick_replies = QuickReplyResponse()
    for arch in architectures:
        quick_replies.add_reply(arch, 'select-architecture', [arch])

    return [divider, question, quick_replies.__repr__()]


async def elicitation_architecture_followup_handler(result) -> List[Dict]:
    return await elicitation_architecture_handler(result)


async def elicitation_architecture_default_handler(result) -> List[Dict]:
    architectures = []
    await sync_to_async(fetch_architectures)(architectures)

    result = set_context_parameters(result, 'c-config', {'arch-file': random_selection(architectures)})

    return await elicitation_architecture_handler(result)
