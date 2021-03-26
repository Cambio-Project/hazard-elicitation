from google.api_core.exceptions import InvalidArgument

from dialogflow_backend.dialogflow.intents import INTENT_HANDLERS, INTENT_PROCESSING_ERROR
from dialogflow_backend.dialogflow.response_types import TextResponse, CardResponse
from util.log import error, warning, debug
from util.text.ids import INTENT_KB_NAME
from util.text.text import text


async def create_response(result):
    """
    Gets a detected intent and calls the intent handler of the corresponding intent.
    The intent handler will produce either a text message (chat message, rich content)
    or a non-text message (empty response, action response).
    @param result:
    """
    response_data = None
    intent = result.query_result.intent.display_name

    debug(intent)

    if intent in INTENT_HANDLERS:
        try:
            # Call intent handler by intent name.
            response_data = await INTENT_HANDLERS[intent](result)
        except InvalidArgument as e:
            error('Intent handler for "{}" produced invalid argument: {}'.format(intent, e))
    elif result.query_result.action:
        # Smalltalk intent is handled by dialogflow.
        response_data = [TextResponse.create(result.query_result.fulfillment_text)]
    elif result.query_result.knowledge_answers:
        # Match in knowledge base was detected.
        response_data = await INTENT_HANDLERS[text(INTENT_KB_NAME)](result)
    else:
        warning('No intent handler found for "{}".'.format(intent))

    # Create default response.
    if not response_data:
        response_data = [TextResponse.create(text(INTENT_PROCESSING_ERROR))]

    return response_data
