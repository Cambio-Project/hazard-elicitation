from util.text.ids import *

TEXT = {
    DEFAULT:                          '...',

    # Fallback
    INTENT_PROCESSING_ERROR:          'Ops something went wrong.',

    # Default
    INTENT_EMPTY_NAME:                'Default-Empty',
    INTENT_FALLBACK_NAME:             'Default-Fallback',
    INTENT_FALLBACK_TEXT:             [
        'That doesn\'t compute. Maybe you can rephrase your sentence?',
        'I don\'t know what you mean. Can you elaborate?',
        'I missed what you said. What was that?',
        'Sorry, could you say that in a different way?',
        'Sorry, I didn\'t get that. Can you rephrase?',
        'Sorry, what was that?',
        'I didn\'t get that. Can you try something different?',
        'That doesn\'t really make sense to me.',
        'Maybe try something different?.'
    ],
    INTENT_HELP_NAME:                 'Default-Help',
    INTENT_HELP_TEXT:                 [
        str('Hang on, help is on it\'s way!'
            'I am a chatbot that helps to elicit resilience scenarios.')
    ],
    INTENT_WELCOME_NAME:              'Default-Welcome',
    INTENT_WELCOME_TEXT:              [
        'Hi! How are you doing?',
        'Hello! How can I help you?',
        'Good day! What can I do for you?',
        'Greetings! How may I help you?'
    ],

    # Elicitation
    INTENT_ELICITATION_QUESTION_NAME: 'Elicitation-Question',
    INTENT_ELICITATION_QUESTION_TEXT: [
        'Is the service {} essential for the service to run optimally?'
    ],

    # Util
    INTENT_COMMAND_CONFIG_NAME:       'Command-Config',
    INTENT_COMMAND_CONFIG_LIST_NAME:  'Command-Config-List',
    INTENT_COMMAND_MANAGE_NAME:       'Command-Manage',
    INTENT_COMMAND_MANAGE_LIST_NAME:  'Command-Manage-List',

    # Extra
    INTENT_FACT_NAME:                 'Extra-Fact',
    INTENT_JOKE_NAME:                 'Extra-Joke'
}
