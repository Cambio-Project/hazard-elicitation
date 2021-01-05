from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

import uuid

import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

from dialogflow_backend.intents.intents import INTENTS
from dialogflow_backend.intents.intent_handler import *
from hazard_elicitation.settings import KEYS


def test(request: HttpRequest) -> HttpResponse:
    return render(request, 'html/test.html')


async def bot(request: HttpRequest) -> HttpResponse:
    return render(request, 'html/bot.html')


async def dialogflow_webhook(request: HttpRequest) -> HttpResponse:
    DIALOGFLOW_PROJECT_ID = KEYS.get('dialogflow_project')
    DIALOGFLOW_LANGUAGE_CODE = 'en'
    SESSION_ID = uuid.uuid4()

    text_to_be_analyzed = json.loads(request.body).get('queryResult', {}).get('queryText', '')

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        print("Query text:", response.query_result.query_text)
        print("Detected intent:", response.query_result.intent.display_name)
        print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        print("Fulfillment text:", response.query_result.fulfillment_text)
        intent = response.query_result.intent.display_name
        if intent in INTENTS:
            if intent == '0-fallback':
                response_text = await fallback_handler()
            elif intent == '0-welcome':
                response_text = await welcome_handler()
            elif intent == 'x-joke':
                response_text = await joke_handler()
            else:
                response_text = 'Nada'
        else:
            response_text = response.query_result.fulfillment_text
    except InvalidArgument:
        response_text = 'Default Text: Something went wrong'

    text = {
        'type':    'text',
        'payload': response_text
    }

    return HttpResponse('ok')
