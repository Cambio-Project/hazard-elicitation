import uuid

import dialogflow_v2 as df

from hazard_elicitation.settings import KEYS
from util.text.languages import LanguageConfig


class DialogFlowClient:
    LANGUAGE = LanguageConfig.LANGUAGE
    PROJECT = KEYS.get('dialogflow_project')

    @staticmethod
    def detect_intent(text: str, session: str = uuid.uuid4()):
        session_client = df.SessionsClient()
        session = session_client.session_path(DialogFlowClient.PROJECT, session)
        text_input = df.types.TextInput(text=text, language_code=DialogFlowClient.LANGUAGE)
        query_input = df.types.QueryInput(text=text_input)
        return session_client.detect_intent(session=session, query_input=query_input)
