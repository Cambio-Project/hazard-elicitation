import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from software_architecture_extraction.source.extractor.models.study import InteractionModel
from dialogflow_backend.dialogflow.client import DialogFlowClient
from dialogflow_backend.dialogflow.response_handler import create_response
from dialogflow_backend.dialogflow.response_types import ActionResponse
from dialogflow_backend.dialogflow.util import next_event
from hazard_elicitation.settings import COLLECT_STUDY
from util.log import warning, error, debug
from util.tracing import add_trace


class DFWebsocket(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Accept WS connection.
        """
        await self.channel_layer.group_add('dialogflow', self.channel_name)

        await self.accept()
        debug('Accept connection.')

    async def disconnect(self, close_code):
        """
        Disconnect WS connection
        """
        await self.channel_layer.group_discard('dialogflow', self.channel_name)

        debug('Disconnect connection.')

    async def receive(self, **kwargs):
        """
        WS has send data.
        """
        # Extract text data from the message.
        data = json.loads(kwargs.get('text_data'))

        if not data:
            warning('No text data received.')
            return

        msg_type = data.get('type')
        if not msg_type:
            warning('No message type defined.')
            return

        # Look for matching message handlers (text input, event input).
        if not hasattr(self, msg_type):
            warning('No handler for message type "{}"'.format(msg_type))
            return

        await getattr(self, msg_type)(data.get('data'), data.get('contexts'), data.get('uuid'))

    @add_trace(True)
    async def dialogflow_text_input(self, data: str, contexts: list, uuid: str):
        """
        Processes text input from a user and detects an intent.
        A response is triggered based on the detected intent name.
        @param data: str    The text input send from an application.
        @param contexts:    List of contexts.
        @param uuid:        UUID created on client.
        """
        result = None

        try:
            if COLLECT_STUDY:
                await sync_to_async(InteractionModel.objects.create)(session_id=uuid, content=data, actor="User")

            result = DialogFlowClient.detect_intent(data, contexts, uuid)

            await self.response_handler(result)
        except Exception as e:
            error('Something went wrong during text input processing: {}'.format(e))
            return [ActionResponse.create('command', ['event', next_event(result)])]

    @add_trace(True)
    async def dialogflow_event_input(self, data: str, contexts: list, uuid: str):
        """
        Processes an event and triggers a response based on the detected intent.
        @param data: str    The event input send from an application.
        @param contexts:    List of contexts.
        @param uuid:        UUID created on client.
        """
        result = None

        try:
            if COLLECT_STUDY:
                await sync_to_async(InteractionModel.objects.create)(session_id=uuid, content=data, actor="User")

            result = DialogFlowClient.detect_event(data, contexts, uuid)

            await self.response_handler(result)
        except Exception as e:
            error('Something went wrong during event input processing: {}'.format(e))
            return [ActionResponse.create('command', ['event', next_event(result)])]

    @add_trace(True)
    async def response_handler(self, result):
        """
        Gets a DF intent detection and creates a response message for the WS connection.
        @param result:  DF result of intent detection.
        """
        response_data = await create_response(result)

        if COLLECT_STUDY:
            session_name = result.query_result.output_contexts[0].name
            session = session_name[session_name.find('sessions') + 9:session_name.rfind('/contexts')]
            text = result.query_result.intent.display_name

            await sync_to_async(InteractionModel.objects.create)(session_id=session, content=text, actor="Bot")

        await self.send(json.dumps({
            'type': 'dialogflow_response',
            'data': response_data
        }))
