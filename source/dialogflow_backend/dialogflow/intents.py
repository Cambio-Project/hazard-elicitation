from util.text.en import TEXT
from dialogflow_backend.dialogflow.intent_handler import *

INTENT_HANDLERS = {
    TEXT[INTENT_FALLBACK_NAME]:             fallback_handler,
    TEXT[INTENT_HELP_NAME]:                 help_handler,
    TEXT[INTENT_WELCOME_NAME]:              welcome_handler,
    TEXT[INTENT_ELICITATION_QUESTION_NAME]: elicitation_question_handler,
    TEXT[INTENT_CONFIG_NAME]:               config_handler,
    TEXT[INTENT_CONFIG_LIST_NAME]:          config_list_handler,
    TEXT[INTENT_FACT_NAME]:                 fact_handler,
    TEXT[INTENT_JOKE_NAME]:                 joke_handler,
}
