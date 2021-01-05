from channels.generic.websocket import AsyncWebsocketConsumer
from google.api_core.exceptions import InvalidArgument

from dialogflow_backend.client import DialogFlowClient
from dialogflow_backend.intents.intents import INTENTS
from dialogflow_backend.intents.intent_handler import *


class DFWebsocket(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('dialogflow', self.channel_name)

        await self.accept()
        print('acc')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('dialogflow', self.channel_name)

        print('disc')

    async def receive(self, **kwargs):
        data = json.loads(kwargs.get('text_data'))

        if not data:
            print('no text')
            return

        msg_type = data.get('type')
        if not msg_type:
            print('no message type')
            return

        if not hasattr(self, msg_type):
            print('no handler for ', msg_type)
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

            # print(intent,
            #       all_parameters_present,
            #       action,
            #       contexts,
            #       parameters,
            #       confidence,
            #       sentiment_score,
            #       sentiment_magnitude, sep='\n')

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
                response_data = {
                    'type':    'text',
                    'payload': result.query_result.fulfillment_text
                }
        except InvalidArgument:
            pass

        await self.send(json.dumps({
            'type': 'dialogflow_response',
            'data': [
                response_data,
                # quick_reply,
                # card,
                # accordion
            ]
        }))
