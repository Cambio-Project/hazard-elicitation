from util.text.en import TEXT
from dialogflow_backend.dialogflow.intent_handlers.default import *
from dialogflow_backend.dialogflow.intent_handlers.guide import *
from dialogflow_backend.dialogflow.intent_handlers.welcome import *
from dialogflow_backend.dialogflow.intent_handlers.extra import *
from dialogflow_backend.dialogflow.intent_handlers.elicitation.architecture import *
from dialogflow_backend.dialogflow.intent_handlers.elicitation.component import *
from dialogflow_backend.dialogflow.intent_handlers.elicitation.description import *
from dialogflow_backend.dialogflow.intent_handlers.elicitation.measure import *
from dialogflow_backend.dialogflow.intent_handlers.elicitation.response import *
from dialogflow_backend.dialogflow.intent_handlers.elicitation.scenario import *
from dialogflow_backend.dialogflow.intent_handlers.elicitation.stimulus import *

INTENT_HANDLERS = {
    TEXT[INTENT_CLEAR_NAME]:                                     empty_handler,
    TEXT[INTENT_EMPTY_NAME]:                                     empty_handler,
    TEXT[INTENT_FALLBACK_NAME]:                                  fallback_handler,
    TEXT[INTENT_BYE_NAME]:                                       bye_handler,
    TEXT[INTENT_HELP_NAME]:                                      help_handler,
    TEXT[INTENT_KB_NAME]:                                        kb_handler,
    TEXT[INTENT_GUIDE_NAME]:                                     guide_handler,
    TEXT[INTENT_GUIDE_OPTION_NAME]:                              guide_option_handler,
    TEXT[INTENT_GUIDE_CONFIRM_NAME]:                             guide_confirm_handler,
    TEXT[INTENT_WELCOME_NAME]:                                   welcome_handler,
    TEXT[INTENT_WELCOME_CONFIRM_NAME]:                           welcome_confirm_handler,
    TEXT[INTENT_WELCOME_DECLINE_NAME]:                           welcome_decline_handler,
    TEXT[INTENT_WELCOME_CONTINUE_NAME]:                          welcome_continue_handler,
    TEXT[INTENT_ELICITATION_ARCHITECTURE_NAME]:                  elicitation_architecture_handler,
    TEXT[INTENT_ELICITATION_ARCHITECTURE_FOLLOWUP_NAME]:         elicitation_architecture_followup_handler,
    TEXT[INTENT_ELICITATION_ARCHITECTURE_DEFAULT_NAME]:          elicitation_architecture_default_handler,
    TEXT[INTENT_ELICITATION_COMPONENT_NAME]:                     elicitation_component_handler,
    TEXT[INTENT_ELICITATION_COMPONENT_FOLLOWUP_NAME]:            elicitation_component_followup_handler,
    TEXT[INTENT_ELICITATION_COMPONENT_DEFAULT_NAME]:             elicitation_component_default_handler,
    TEXT[INTENT_ELICITATION_STIMULUS_NAME]:                      elicitation_stimuli_handler,
    TEXT[INTENT_ELICITATION_STIMULUS_FOLLOWUP_NAME]:             elicitation_stimuli_followup_handler,
    TEXT[INTENT_ELICITATION_STIMULUS_DEFAULT_NAME]:              elicitation_stimuli_default_handler,
    TEXT[INTENT_ELICITATION_STIMULUS_SOURCE_NAME]:               elicitation_stimuli_source_handler,
    TEXT[INTENT_ELICITATION_STIMULUS_SOURCE_FOLLOWUP_NAME]:      elicitation_stimuli_source_followup_handler,
    TEXT[INTENT_ELICITATION_STIMULUS_SOURCE_DEFAULT_NAME]:       elicitation_stimuli_source_default_handler,
    TEXT[INTENT_ELICITATION_STIMULUS_ENVIRONMENT_NAME]:          elicitation_stimuli_environment_handler,
    TEXT[INTENT_ELICITATION_STIMULUS_ENVIRONMENT_FOLLOWUP_NAME]: elicitation_stimuli_environment_followup_handler,
    TEXT[INTENT_ELICITATION_STIMULUS_ENVIRONMENT_DEFAULT_NAME]:  elicitation_stimuli_environment_default_handler,
    TEXT[INTENT_ELICITATION_RESPONSE_NAME]:                      elicitation_response_handler,
    TEXT[INTENT_ELICITATION_RESPONSE_FOLLOWUP_NAME]:             elicitation_response_followup_handler,
    TEXT[INTENT_ELICITATION_RESPONSE_DEFAULT_NAME]:              elicitation_response_default_handler,
    TEXT[INTENT_ELICITATION_MEASURE_NAME]:                       elicitation_measure_handler,
    TEXT[INTENT_ELICITATION_MEASURE_NORMAL_NAME]:                elicitation_measure_normal_handler,
    TEXT[INTENT_ELICITATION_MEASURE_NORMAL_FOLLOWUP_NAME]:       elicitation_measure_normal_followup_handler,
    TEXT[INTENT_ELICITATION_MEASURE_NORMAL_DEFAULT_NAME]:        elicitation_measure_normal_default_handler,
    TEXT[INTENT_ELICITATION_MEASURE_CASES_NAME]:                 elicitation_measure_cases_handler,
    TEXT[INTENT_ELICITATION_MEASURE_CASES_FOLLOWUP_NAME]:        elicitation_measure_cases_followup_handler,
    TEXT[INTENT_ELICITATION_MEASURE_CASES_DEFAULT_NAME]:         elicitation_measure_cases_default_handler,
    TEXT[INTENT_ELICITATION_MEASURE_RECOVERY_NAME]:              elicitation_measure_recovery_handler,
    TEXT[INTENT_ELICITATION_MEASURE_RECOVERY_FOLLOWUP_NAME]:     elicitation_measure_recovery_followup_handler,
    TEXT[INTENT_ELICITATION_MEASURE_RECOVERY_DEFAULT_NAME]:      elicitation_measure_recovery_default_handler,
    TEXT[INTENT_ELICITATION_DESCRIPTION_NAME]:                   elicitation_description_handler,
    TEXT[INTENT_ELICITATION_DESCRIPTION_FOLLOWUP_NAME]:          elicitation_description_followup_handler,
    TEXT[INTENT_ELICITATION_DESCRIPTION_DEFAULT_NAME]:           elicitation_description_default_handler,
    TEXT[INTENT_ELICITATION_SAVE_SCENARIO_NAME]:                 elicitation_save_scenario_handler,
    TEXT[INTENT_ELICITATION_SAVE_SCENARIO_CONFIRM_NAME]:         elicitation_save_scenario_confirm_handler,
    TEXT[INTENT_ELICITATION_NEXT_STEP_NAME]:                     elicitation_next_step_handler,
    TEXT[INTENT_ELICITATION_NEXT_STEP_CONFIRM_NAME]:             elicitation_next_step_confirm_handler,
    TEXT[INTENT_ELICITATION_NEXT_STEP_DECLINE_NAME]:             elicitation_next_step_decline_handler,
    TEXT[INTENT_FACT_NAME]:                                      fact_handler,
    TEXT[INTENT_JOKE_NAME]:                                      joke_handler,
}
