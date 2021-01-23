TEXT_ID = 0


def text_id():
    global TEXT_ID
    TEXT_ID += 1
    return TEXT_ID


DEFAULT = text_id()

# Default response text
INTENT_PROCESSING_ERROR = text_id()

# Default intents
INTENT_FALLBACK_NAME = text_id()
INTENT_FALLBACK_TEXT = text_id()
INTENT_HELP_NAME = text_id()
INTENT_HELP_TEXT = text_id()
INTENT_WELCOME_NAME = text_id()
INTENT_WELCOME_TEXT = text_id()

# Elicitation intents
INTENT_ELICITATION_QUESTION_NAME = text_id()
INTENT_ELICITATION_QUESTION_TEXT = text_id()

# Util intents
INTENT_COMMAND_CONFIG_NAME = text_id()
INTENT_COMMAND_CONFIG_LIST_NAME = text_id()
INTENT_COMMAND_MANAGE_NAME = text_id()
INTENT_COMMAND_MANAGE_LIST_NAME = text_id()

# Extra intents
INTENT_FACT_NAME = text_id()
INTENT_JOKE_NAME = text_id()
