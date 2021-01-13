from channels.generic.websocket import AsyncWebsocketConsumer
from google.api_core.exceptions import InvalidArgument

from dialogflow_backend.dialogflow.client import DialogFlowClient
from dialogflow_backend.dialogflow.intents import INTENT_HANDLERS
from dialogflow_backend.dialogflow.intent_handler import *
from util.log import info, warning, error, debug
from util.text.text import text


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
                if intent == text(INTENT_FALLBACK_NAME):
                    response_data = await fallback_handler()
                elif intent == text(INTENT_FALLBACK_GIBBERISH_NAME):
                    response_data = await fallback_gibberish_handler()
                elif intent == text(INTENT_FALLBACK_INSULT_NAME):
                    response_data = await fallback_insult_handler()
                elif intent == text(INTENT_HELP_NAME):
                    response_data = await help_handler()
                elif intent == text(INTENT_WELCOME_NAME):
                    response_data = await welcome_handler()
                elif intent == text(INTENT_ELICITATION_QUESTION_NAME):
                    response_data = await elicitation_question_handler()
                elif intent == text(INTENT_FACT_NAME):
                    response_data = await fact_handler()
                elif intent == text(INTENT_JOKE_NAME):
                    response_data = await joke_handler()

            else:
                response_data = [{
                    'type':    'text',
                    'payload': result.query_result.fulfillment_text or 'EMPTY TEXT'
                }]

            # TODO remove
            add_intent = lambda r: {'type': r['type'], 'intent': intent, 'payload': r['payload']}
            response_data = list(map(add_intent, response_data))

        except InvalidArgument:
            error('DF WS intent handler produced invalid argument.')
            pass

        await self.send(json.dumps({
            'type': 'dialogflow_response',
            'data': response_data
        }))
