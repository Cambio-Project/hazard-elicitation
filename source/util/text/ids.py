TEXT_ID = 0


def text_id():
    global TEXT_ID
    TEXT_ID += 1
    return TEXT_ID


DEFAULT = text_id()

# Knowledge base answers
INTENT_KB_NAME = text_id()

# Stimulus & Response & Response measure values
STIMULUS_RESPONSE_TEXTS = text_id()

# Default response text
INTENT_PROCESSING_ERROR = text_id()

# Default intents
INTENT_EMPTY_NAME = text_id()
INTENT_CLEAR_NAME = text_id()
INTENT_FALLBACK_NAME = text_id()
INTENT_FALLBACK_TEXT = text_id()
INTENT_BYE_NAME = text_id()
INTENT_BYE_TEXT = text_id()
INTENT_BYE_QUESTIONNAIRE = text_id()
INTENT_HELP_NAME = text_id()
INTENT_HELP_TEXT = text_id()
INTENT_GUIDE_NAME = text_id()
INTENT_GUIDE_TEXT = text_id()
INTENT_GUIDE_CONTINUE_TEXT = text_id()
INTENT_GUIDE_CONTINUE_CONFIRM_TEXT = text_id()
INTENT_GUIDE_OPTIONS = text_id()
INTENT_GUIDE_EXPLANATIONS = text_id()
INTENT_GUIDE_OPTION_NAME = text_id()
INTENT_GUIDE_CONFIRM_NAME = text_id()
INTENT_WELCOME_NAME = text_id()
INTENT_WELCOME_TEXT = text_id()
INTENT_WELCOME_RESUME_TEXT = text_id()
INTENT_WELCOME_YES_TEXT = text_id()
INTENT_WELCOME_NO_TEXT = text_id()
INTENT_WELCOME_CONFIRM_NAME = text_id()
INTENT_WELCOME_DECLINE_NAME = text_id()
INTENT_WELCOME_CONTINUE_NAME = text_id()

# Elicitation intents
INTENT_ELICITATION_ARCHITECTURE_NAME = text_id()
INTENT_ELICITATION_ARCHITECTURE_TEXT = text_id()
INTENT_ELICITATION_ARCHITECTURE_FOLLOWUP_NAME = text_id()
INTENT_ELICITATION_ARCHITECTURE_DEFAULT_NAME = text_id()
INTENT_ELICITATION_COMPONENT_NAME = text_id()
INTENT_ELICITATION_COMPONENT_TEXT = text_id()
INTENT_ELICITATION_COMPONENT_MISSING_TEXT = text_id()
INTENT_ELICITATION_COMPONENT_SERVICE_TEXT = text_id()
INTENT_ELICITATION_COMPONENT_OPERATION_TEXT = text_id()
INTENT_ELICITATION_COMPONENT_FOLLOWUP_NAME = text_id()
INTENT_ELICITATION_COMPONENT_DEFAULT_NAME = text_id()
INTENT_ELICITATION_STIMULUS_NAME = text_id()
INTENT_ELICITATION_STIMULUS_TEXT = text_id()
INTENT_ELICITATION_STIMULUS_FOLLOWUP_NAME = text_id()
INTENT_ELICITATION_STIMULUS_DEFAULT_NAME = text_id()
INTENT_ELICITATION_STIMULUS_SOURCE_NAME = text_id()
INTENT_ELICITATION_STIMULUS_SOURCE_TEXT = text_id()
INTENT_ELICITATION_STIMULUS_SOURCE_FOLLOWUP_NAME = text_id()
INTENT_ELICITATION_STIMULUS_SOURCE_DEFAULT_NAME = text_id()
INTENT_ELICITATION_STIMULUS_ENVIRONMENT_NAME = text_id()
INTENT_ELICITATION_STIMULUS_ENVIRONMENT_TEXT = text_id()
INTENT_ELICITATION_STIMULUS_ENVIRONMENT_FOLLOWUP_NAME = text_id()
INTENT_ELICITATION_STIMULUS_ENVIRONMENT_DEFAULT_NAME = text_id()
INTENT_ELICITATION_RESPONSE_NAME = text_id()
INTENT_ELICITATION_RESPONSE_TEXT = text_id()
INTENT_ELICITATION_RESPONSE_FOLLOWUP_NAME = text_id()
INTENT_ELICITATION_RESPONSE_DEFAULT_NAME = text_id()
INTENT_ELICITATION_MEASURE_NAME = text_id()
INTENT_ELICITATION_MEASURE_TEXT = text_id()
INTENT_ELICITATION_MEASURE_NORMAL_NAME = text_id()
INTENT_ELICITATION_MEASURE_NORMAL_TEXT = text_id()
INTENT_ELICITATION_MEASURE_NORMAL_FOLLOWUP_NAME = text_id()
INTENT_ELICITATION_MEASURE_NORMAL_DEFAULT_NAME = text_id()
INTENT_ELICITATION_MEASURE_CASES_NAME = text_id()
INTENT_ELICITATION_MEASURE_CASES_SERVICE_TEXT = text_id()
INTENT_ELICITATION_MEASURE_CASES_OPERATION_TEXT = text_id()
INTENT_ELICITATION_MEASURE_CASES_FOLLOWUP_NAME = text_id()
INTENT_ELICITATION_MEASURE_CASES_DEFAULT_NAME = text_id()
INTENT_ELICITATION_MEASURE_RECOVERY_NAME = text_id()
INTENT_ELICITATION_MEASURE_RECOVERY_TEXT = text_id()
INTENT_ELICITATION_MEASURE_RECOVERY_FOLLOWUP_NAME = text_id()
INTENT_ELICITATION_MEASURE_RECOVERY_DEFAULT_NAME = text_id()
INTENT_ELICITATION_DESCRIPTION_NAME = text_id()
INTENT_ELICITATION_DESCRIPTION_TEXT = text_id()
INTENT_ELICITATION_DESCRIPTION_FOLLOWUP_NAME = text_id()
INTENT_ELICITATION_DESCRIPTION_DEFAULT_NAME = text_id()
INTENT_ELICITATION_DESCRIPTION_QUICK_RESPONSE = text_id()
INTENT_ELICITATION_SAVE_SCENARIO_NAME = text_id()
INTENT_ELICITATION_SAVE_SCENARIO_TEXT = text_id()
INTENT_ELICITATION_SUMMARY_SERVICE_MEASURE_TEXT = text_id()
INTENT_ELICITATION_SUMMARY_OPERATION_MEASURE_TEXT = text_id()
INTENT_ELICITATION_SAVE_SCENARIO_CONTINUE_TEXT = text_id()
INTENT_ELICITATION_SAVE_SCENARIO_SAVE_TEXT = text_id()
INTENT_ELICITATION_SAVE_SCENARIO_SAVE_CONFIRM_TEXT = text_id()
INTENT_ELICITATION_SAVE_SCENARIO_MODIFY_OPTIONS = text_id()
INTENT_ELICITATION_SAVE_SCENARIO_CONFIRM_NAME = text_id()
INTENT_ELICITATION_NEXT_STEP_NAME = text_id()
INTENT_ELICITATION_NEXT_STEP_TEXT = text_id()
INTENT_ELICITATION_NEXT_STEP_EXIT_TEXT = text_id()
INTENT_ELICITATION_NEXT_STEP_CONTINUE_TEXT = text_id()
INTENT_ELICITATION_NEXT_STEP_CONFIRM_NAME = text_id()
INTENT_ELICITATION_NEXT_STEP_DECLINE_NAME = text_id()

# Extra intents
INTENT_FACT_NAME = text_id()
INTENT_FACT_TEXT = text_id()
INTENT_JOKE_NAME = text_id()
INTENT_JOKE_TEXT = text_id()
