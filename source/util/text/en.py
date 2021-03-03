from util.text.ids import *

TEXT = {
    DEFAULT:                                            '...',

    # Fallback
    INTENT_PROCESSING_ERROR:                            'Ops something went wrong.',

    # Default
    INTENT_EMPTY_NAME:                                  'Default-Empty',
    INTENT_FALLBACK_NAME:                               'Default-Fallback',
    INTENT_FALLBACK_TEXT:                               [
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
    INTENT_HELP_NAME:                                   'Default-Help',
    INTENT_HELP_TEXT:                                   [
        str('Hang on, help is on it\'s way!'
            'I am a chatbot that helps to elicit resilience scenarios.')
    ],
    INTENT_WELCOME_NAME:                                'Default-Welcome',
    INTENT_WELCOME_TEXT:                                str(
        'Hey there! &#x1F44B;<br><br>'
        'I am a chatbot and I will help you to elicit <b>resilience scenarios</b>. '
        'For each scenario we will go through the following steps:<br>'
        '<ol>'
        '<li>Select an architecture to analyze</li>'
        '<li>Select a <b>component</b> of the architecture</li>'
        '<li>Specify a <b>response</b> and a <b>response measurement</b></li>'
        '<li>Save or create another <b>resilience scenario</b></li>'
        '</ol>'
        'Are you ready?'
    ),

    # Elicitation
    INTENT_ELICITATION_SELECT_ARCHITECTURE_NAME:        'Elicitation-Select-Architecture',
    INTENT_ELICITATION_SELECT_ARCHITECTURE_TEXT:        str(
        '<h6>Step 1 - Select an architecture</h6>'
        'Below you are given a list of architectures. '
        'Please select one architecture.'
    ),
    INTENT_ELICITATION_SELECT_COMPONENT_NAME:           'Elicitation-Select-Component',
    INTENT_ELICITATION_SELECT_COMPONENT_TEXT:           str(
        '<h6>Step 2 - Select a component for {}</h6>'
        'I created a selection for you to choose from. '
        'Please select one component.'
    ),
    INTENT_ELICITATION_SELECT_COMPONENT_TEXT_SERVICE:   'Here are the services to choose from ...',
    INTENT_ELICITATION_SELECT_COMPONENT_TEXT_OPERATION: 'Here are the operations to choose from ...',
    INTENT_ELICITATION_SPECIFY_RESPONSE_NAME:           'Elicitation-Specify-Response',
    INTENT_ELICITATION_SPECIFY_RESPONSE_TEXT:           str(
        '<h6>Step 3 - Specify response and response measure for {}</h6>'
        ''
    ),
    INTENT_ELICITATION_QUESTION_NAME:                   'Elicitation-Question',
    INTENT_ELICITATION_QUESTION_TEXT:                   [
        'Is the service {} essential for the service to run optimally?'
    ],

    # Util
    INTENT_COMMAND_CONFIG_NAME:                         'Command-Config',
    INTENT_COMMAND_CONFIG_LIST_NAME:                    'Command-Config-List',
    INTENT_COMMAND_MANAGE_NAME:                         'Command-Manage',
    INTENT_COMMAND_MANAGE_LIST_NAME:                    'Command-Manage-List',

    # Extra
    INTENT_FACT_NAME:                                   'Extra-Fact',
    INTENT_FACT_TEXT:                                   [
        'I didn\'t know that one &#x1F446;.',
        'Hm, very interesting.',
        'Who would have thought...'
    ],
    INTENT_JOKE_NAME:                                   'Extra-Joke',
    INTENT_JOKE_TEXT:                                   [
        'Yeah, that\'s a good one &#x1F604;.',
        'Yikes &#x1F923;.',
        'Not so sure about that one &#x1F928;.'
    ]
}
