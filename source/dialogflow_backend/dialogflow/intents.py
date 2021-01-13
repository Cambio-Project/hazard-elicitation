from util.text.ids import *
from util.text.en import TEXT

INTENT_HANDLERS = {
    TEXT[INTENT_FALLBACK_NAME]:             'fallback_handler',
    TEXT[INTENT_FALLBACK_GIBBERISH_NAME]:   'fallback_gibberish_handler',
    TEXT[INTENT_FALLBACK_INSULT_NAME]:      'fallback_insult_handler',
    TEXT[INTENT_HELP_NAME]:                 'help_handler',
    TEXT[INTENT_WELCOME_NAME]:              'welcome_handler',
    TEXT[INTENT_ELICITATION_QUESTION_NAME]: 'fact_handler',
    TEXT[INTENT_FACT_NAME]:                 'fact_handler',
    TEXT[INTENT_JOKE_NAME]:                 'joke_handler',
}
