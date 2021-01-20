from channels.generic.websocket import AsyncWebsocketConsumer
from google.api_core.exceptions import InvalidArgument

from dialogflow_backend.dialogflow import intent_handler
from dialogflow_backend.dialogflow.intent_handler import *
from dialogflow_backend.dialogflow.client import DialogFlowClient
from dialogflow_backend.dialogflow.intents import INTENT_HANDLERS
from util.log import info, warning, error, debug


class DFWebsocket(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('dialogflow', self.channel_name)

        await self.accept()
        info('Accept connection.')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('dialogflow', self.channel_name)

        info('Disconnect connection.')

    async def receive(self, **kwargs):
        data = json.loads(kwargs.get('text_data'))

        if not data:
            warning('No text data received.')
            return

        msg_type = data.get('type')
        if not msg_type:
            warning('No message type defined.')
            return

        if not hasattr(self, msg_type):
            warning('No handler for message type "{}"'.format(msg_type))
            return

        await getattr(self, msg_type)(data.get('data'))

    async def dialogflow_request(self, data: str):
        response_data = None

        try:
            result = DialogFlowClient.detect_intent(data)

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

            if intent in INTENT_HANDLERS:
                try:
                    # Call intent handler
                    response_data = await INTENT_HANDLERS[intent](result)
                except InvalidArgument as e:
                    error('Intent handler for "{}" produced invalid argument: {}'.format(intent, e))
            else:
                warning('No intent handler found for "{}".'.format(intent))

        except Exception as e:
            error('Something went wrong during intent processing: {}'.format(e))

        # Create default response.
        if not response_data:
            response = TextMessage()
            response.text = 'Ops something wen wrong.'
            response_data = [response.__repr__()]

        debug(response_data)

        await self.send(json.dumps({
            'type': 'dialogflow_response',
            'data': response_data
        }))
