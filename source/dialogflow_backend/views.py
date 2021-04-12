import uuid
import zipfile

from django.http import JsonResponse, HttpResponse

from dialogflow_backend.dialogflow.client import DialogFlowClient
from dialogflow_backend.dialogflow.response_handler import create_response
from util.log import error

from architecture_extraction_backend.models.study import InteractionModel, ScenarioModel


async def detect_intent(request):
    text = request.GET.get('text', '')
    contexts = request.GET.get('contexts', [{}])

    df_response = DialogFlowClient.detect_intent(text, contexts, str(uuid.uuid4()))
    response_data = await create_response(df_response)
    return JsonResponse(response_data, safe=False)


async def detect_event(request):
    event = request.GET.get('event', '')
    contexts = request.GET.get('contexts', [{}])

    df_response = DialogFlowClient.detect_event(event, contexts, str(uuid.uuid4()))
    response_data = await create_response(df_response)
    return JsonResponse(response_data, safe=False)


def export_study(request):
    try:
        response = HttpResponse(content_type='application/zip')
        archive = zipfile.ZipFile(response, 'w')

        for values in InteractionModel.objects.values('session_id').distinct():
            session_id = values['session_id']

            # Save interaction of each participant
            lines = []
            for obj in InteractionModel.objects \
                    .filter(session_id=session_id) \
                    .values('date', 'actor', 'content'):
                lines += '{},{},{}\n'.format(obj['date'], obj['actor'], obj['content'])
            archive.writestr(session_id + '_interaction.csv', ''.join(lines).encode('utf-8'))

            # Save scenarios for each participant
            lines = []
            for obj in ScenarioModel.objects \
                    .filter(session_id=session_id) \
                    .values('date', 'content'):
                lines += '{},{}\n'.format(obj['date'], obj['content'])
            archive.writestr(session_id + '_scenario.csv', ''.join(lines).encode('utf-8'))

        response['Content-Disposition'] = 'attachment; filename={}'.format('study.zip')
        return response

    except BaseException as e:
        error(e)
        return HttpResponse('Processing error', status=500)
