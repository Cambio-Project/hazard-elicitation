from django.http import JsonResponse

from dialogflow_backend.dialogflow.client import DialogFlowClient
from dialogflow_backend.dialogflow.response_handler import create_response


async def detect_intent(request):
    text = request.GET.get('text', '')
    contexts = request.GET.get('contexts', [{}])

    df_response = DialogFlowClient.detect_intent(text, contexts)
    response_data = await create_response(df_response)
    return JsonResponse(response_data, safe=False)


async def detect_event(request):
    event = request.GET.get('event', '')
    contexts = request.GET.get('contexts', [{}])

    df_response = DialogFlowClient.detect_event(event, contexts)
    response_data = await create_response(df_response)
    return JsonResponse(response_data, safe=False)
