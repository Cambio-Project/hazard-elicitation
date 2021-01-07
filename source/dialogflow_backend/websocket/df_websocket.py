from channels.generic.websocket import AsyncWebsocketConsumer
from google.api_core.exceptions import InvalidArgument

from dialogflow_backend.dialogflow.client import DialogFlowClient
from dialogflow_backend.dialogflow.intents import INTENTS
from dialogflow_backend.dialogflow.intent_handler import *
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
        response_data = {
            'type':    'text',
            'payload': 'Default Text: Something went wrong'
        }

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
                      '- Confidence: {}\n'
                      '- Contexts; {}\n'
                      '- Action: {}\n'
                      '- All parameters present: {}\n'
                      '- Parameters: {}\n'
                      '- Sentiment (Score/Magnitude): {}/{}').format(
                confidence,
                contexts,
                action,
                all_parameters_present,
                parameters,
                sentiment_score,
                sentiment_magnitude,
            ))

            if intent in INTENTS:
                if intent == '0-fallback':
                    response_data = await fallback_handler()
                elif intent == '0-fallback-gibberish':
                    response_data = await fallback_gibberish_handler()
                elif intent == '0-fallback-insult':
                    response_data = await fallback_insult_handler()
                elif intent == '0-help':
                    response_data = await help_handler()
                elif intent == '0-welcome':
                    response_data = await welcome_handler()
                elif intent == 'x-fact':
                    response_data = await fact_handler()
                elif intent == 'x-joke':
                    response_data = await joke_handler()

            else:
                response_data = [{
                    'type':    'text',
                    'payload': result.query_result.fulfillment_text
                }]

        except InvalidArgument:
            error('DF WS intent handler produced invalid argument.')
            pass

        await self.send(json.dumps({
            'type': 'dialogflow_response',
            'data': response_data
        }))
