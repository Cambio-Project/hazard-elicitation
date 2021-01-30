from channels.generic.websocket import AsyncWebsocketConsumer
from google.api_core.exceptions import InvalidArgument

from dialogflow_backend.dialogflow.intent_handler import *
from dialogflow_backend.dialogflow.client import DialogFlowClient
from dialogflow_backend.dialogflow.intents import INTENT_HANDLERS
from util.log import info, warning, error, debug
from util.tracing import add_trace


class DFWebsocket(AsyncWebsocketConsumer):
    @staticmethod
    def debug(result):
        intent = result.query_result.intent.display_name
        action = result.query_result.action
        all_parameters_present = result.query_result.all_required_params_present
        contexts = result.query_result.output_contexts
        parameters = result.query_result.parameters
        confidence = result.query_result.intent_detection_confidence
        sentiment_score = result.query_result.sentiment_analysis_result.query_text_sentiment.score
        sentiment_magnitude = result.query_result.sentiment_analysis_result.query_text_sentiment.magnitude

        debug(str('Intent processing result:\n'
                  '- Name: {}\n'
                  '- Confidence: {}\n'
                  '- Contexts; {}\n'
                  '- Action: {}\n'
                  '- All parameters present: {}\n'
                  '- Parameters: {}\n'
                  '- Sentiment (Score/Magnitude): {}/{}').format(
            intent,
            confidence,
            contexts,
            action,
            all_parameters_present,
            parameters,
            sentiment_score,
            sentiment_magnitude,
        ))

    async def connect(self):
        await self.channel_layer.group_add('dialogflow', self.channel_name)

        await self.accept()
        info('Accept connection.')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('dialogflow', self.channel_name)

        info('Disconnect connection.')

    async def receive(self, **kwargs):
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

        await getattr(self, msg_type)(data.get('data'))

    @add_trace(True)
    async def response_handler(self, result):
        """
        Gets a detected intent and calls the intent handler of the corresponding intent.
        The intent handler will produce either a text message (chat message, rich content)
        or a non-text message (empty response, action response).
        @param result:
        """
        response_data = None
        intent = result.query_result.intent.display_name

        DFWebsocket.debug(result)

        if intent in INTENT_HANDLERS:
            try:
                # Call intent handler by intent name.
                response_data = await INTENT_HANDLERS[intent](result)
            except InvalidArgument as e:
                error('Intent handler for "{}" produced invalid argument: {}'.format(intent, e))
        else:
            warning('No intent handler found for "{}".'.format(intent))

        # Create default response.
        if not response_data:
            response = TextMessage()
            response.text = text(INTENT_PROCESSING_ERROR)
            response_data = [response.__repr__()]

        await self.send(json.dumps({
            'type': 'dialogflow_response',
            'data': response_data
        }))

    @add_trace(True)
    async def dialogflow_text_input(self, data: str):
        """
        Processes text input from a user and detects an intent.
        A response is triggered based on the detected intent name.
        @param data: str
        """
        try:
            await self.response_handler(DialogFlowClient.detect_intent(data))
        except Exception as e:
            error('Something went wrong during text input processing: {}'.format(e))

    @add_trace(True)
    async def dialogflow_event_input(self, data: str):
        """
        Processes an event and triggers a response based on the detected intent.
        @param data: str    The event input send from an application.
        """
        try:
            await self.response_handler(DialogFlowClient.detect_event(data))
        except Exception as e:
            error('Something went wrong during event input processing: {}'.format(e))
