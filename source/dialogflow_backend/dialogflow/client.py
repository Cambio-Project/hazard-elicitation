import uuid

#import dialogflow_v2 as df
import dialogflow_v2beta1 as df
# import google.cloud.dialogflow_v2.types as df_types

from hazard_elicitation.settings import KEYS
from util.text.languages import LanguageConfig


class DialogFlowClient:
    LANGUAGE = LanguageConfig.LANGUAGE
    PROJECT = KEYS.get('dialogflow_project')
    CONTEXT = 'projects/{}/agent/sessions/{}/contexts/{}'
    KB = 'projects/{}/knowledgeBases/{}'
    AUDIO_ENCODING = df.types.audio_config_pb2.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    AUDIO_SAMPLE_RATE = 48000

    @staticmethod
    def preprocess(external_contexts: list, session_id: str):
        session_client = df.SessionsClient()
        session = session_client.session_path(DialogFlowClient.PROJECT, session_id)

        contexts = []
        for context in external_contexts:
            context_name = context.get('name', '')
            context_parameters = context.get('parameters', {})
            context_lifespan = context.get('lifespan', 1)
            if context_name and context_lifespan:
                parameters = df.types.Struct()
                parameters.update(context_parameters)
                contexts.append(df.types.Context(
                    name=DialogFlowClient.CONTEXT.format(DialogFlowClient.PROJECT, session_id, context_name),
                    lifespan_count=context_lifespan,
                    parameters=parameters))

        return session_client, session, contexts

    @staticmethod
    def detect_event(event: str, external_contexts: list, session_id: str):
        session_client, session, contexts = DialogFlowClient.preprocess(external_contexts, session_id)

        query_params = df.types.QueryParameters(contexts=contexts)
        event_input = df.types.EventInput(name=event, language_code=DialogFlowClient.LANGUAGE)
        query_input = df.types.QueryInput(event=event_input)

        return session_client.detect_intent(
            session=session,
            query_input=query_input,
            query_params=query_params)

    @staticmethod
    def detect_intent(text: str, external_contexts: list, session_id: str):
        session_client, session, contexts = DialogFlowClient.preprocess(external_contexts, session_id)

        sentiment_config = df.types.SentimentAnalysisRequestConfig(analyze_query_text_sentiment=True)
        query_params = df.types.QueryParameters(
            knowledge_base_names=[DialogFlowClient.KB.format(DialogFlowClient.PROJECT, 'NzEwOTcxNzA2MzEwNjU2MDAw')],
            sentiment_analysis_request_config=sentiment_config,
            contexts=contexts)
        text_input = df.types.TextInput(text=text, language_code=DialogFlowClient.LANGUAGE)
        query_input = df.types.QueryInput(text=text_input)

        # Requires fulfillment text in DF UI
        # output_audio_config = df.types.OutputAudioConfig(audio_encoding=DialogFlowClient.AUDIO_ENCODING)

        return session_client.detect_intent(
            session=session,
            query_input=query_input,
            query_params=query_params)
        # output_audio_config=output_audio_config)

    @staticmethod
    def detect_intent_audio(audio: bytes, session: str):
        session_client = df.SessionsClient()
        session = session_client.session_path(DialogFlowClient.PROJECT, session)

        audio_config = df.types.InputAudioConfig(
            audio_encoding=DialogFlowClient.AUDIO_ENCODING,
            language_code=DialogFlowClient.LANGUAGE,
            sample_rate_hertz=DialogFlowClient.AUDIO_SAMPLE_RATE)
        query_input = df.types.QueryInput(audio_config=audio_config)

        sentiment_config = df.types.SentimentAnalysisRequestConfig(analyze_query_text_sentiment=True)
        query_params = df.types.QueryParameters(sentiment_analysis_request_config=sentiment_config)
        output_audio_config = df.types.OutputAudioConfig(audio_encoding=DialogFlowClient.AUDIO_ENCODING)

        return session_client.detect_intent(
            session=session,
            query_input=query_input,
            query_params=query_params,
            input_audio=audio,
            output_audio_config=output_audio_config
        )

    @staticmethod
    def detect_intent_audio_stream(audio: bytes, session: str):
        session_client = df.SessionsClient()
        session = session_client.session_path(DialogFlowClient.PROJECT, session)

        audio_config = df.types.InputAudioConfig(
            audio_encoding=DialogFlowClient.AUDIO_ENCODING,
            language_code=DialogFlowClient.LANGUAGE,
            sample_rate_hertz=DialogFlowClient.AUDIO_SAMPLE_RATE)

        query_input = df.types.QueryInput(audio_config=audio_config)
        requests = [
            df.types.StreamingDetectIntentRequest(session=session, query_input=query_input),
            # TODO parse smaller chunks
            df.types.StreamingDetectIntentRequest(input_audio=audio)
        ]

        return session_client.streaming_detect_intent(requests=requests)
