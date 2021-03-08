from util.text.en import TEXT
from dialogflow_backend.dialogflow.intent_handlers.default import *
from dialogflow_backend.dialogflow.intent_handlers.guide import *
from dialogflow_backend.dialogflow.intent_handlers.welcome import *
from dialogflow_backend.dialogflow.intent_handlers.elicitation import *
from dialogflow_backend.dialogflow.intent_handlers.commands import *
from dialogflow_backend.dialogflow.intent_handlers.extra import *

INTENT_HANDLERS = {
    TEXT[INTENT_EMPTY_NAME]:                                empty_handler,
    TEXT[INTENT_FALLBACK_NAME]:                             fallback_handler,
    TEXT[INTENT_HELP_NAME]:                                 help_handler,
    TEXT[INTENT_GUIDE_NAME]:                                guide_handler,
    TEXT[INTENT_GUIDE_OPTION_NAME]:                         guide_option_handler,
    TEXT[INTENT_GUIDE_CONFIRM_NAME]:                        guide_confirm_handler,
    TEXT[INTENT_WELCOME_NAME]:                              welcome_handler,
    TEXT[INTENT_WELCOME_CONFIRM_NAME]:                      welcome_confirm_handler,
    TEXT[INTENT_WELCOME_DECLINE_NAME]:                      welcome_decline_handler,
    TEXT[INTENT_ELICITATION_SELECT_ARCHITECTURE_NAME]:      elicitation_select_architecture_handler,
    TEXT[INTENT_ELICITATION_SELECT_COMPONENT_NAME]:         elicitation_select_component_handler,
    TEXT[INTENT_ELICITATION_SPECIFY_RESPONSE_NAME]:         elicitation_specify_response_handler,
    TEXT[INTENT_ELICITATION_SPECIFY_RESPONSE_MEASURE_NAME]: elicitation_specify_response_measure_handler,
    TEXT[INTENT_ELICITATION_SAVE_SCENARIO_NAME]:            elicitation_save_scenario_handler,
    TEXT[INTENT_COMMAND_CONFIG_NAME]:                       config_handler,
    TEXT[INTENT_COMMAND_CONFIG_LIST_NAME]:                  config_list_handler,
    TEXT[INTENT_COMMAND_MANAGE_NAME]:                       manage_handler,
    TEXT[INTENT_FACT_NAME]:                                 fact_handler,
    TEXT[INTENT_JOKE_NAME]:                                 joke_handler,
}
