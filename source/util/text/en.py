from util.text.ids import *

TEXT = {
    DEFAULT:                                                   '...',

    # Fallback
    INTENT_PROCESSING_ERROR:                                   'Ops something went wrong.',

    # Default
    INTENT_EMPTY_NAME:                                         'Default-Empty',
    INTENT_FALLBACK_NAME:                                      'Default-Fallback',
    INTENT_FALLBACK_TEXT:                                      [
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
    INTENT_HELP_NAME:                                          'Default-Help',
    INTENT_HELP_TEXT:                                          [
        str('Hang on, help is on it\'s way!'
            'I am a chatbot that helps to elicit resilience scenarios.')
    ],

    # Guide
    INTENT_GUIDE_NAME:                                         'Default-Guide',
    INTENT_GUIDE_TEXT:                                         str(
        'Let us go through this, step by step.<br>'
        'Please select or tell me about which topic you would like to learn more about...'),
    INTENT_GUIDE_OPTIONS:                                      {
        'Architecture': {
            'text':  str(
                'An architecture is constructed from the result of a '
                '<a class="link" href="https://en.wikipedia.org/wiki/Tracing_(software)" target="_blank">'
                'tracing tool</a> analysis. This tool can understand and analyze traces from either '
                '<a class="link" href="https://www.jaegertracing.io/" target="_blank">Jaeger</a> or '
                '<a class="link" href="https://zipkin.io/" target="_blank">Zipkin</a>.'),
            'link':  {
                'text': 'Read more here',
                'url':  'https://en.wikipedia.org/wiki/Tracing_(software)'
            },
            'image': 'static/img/guide/arch.png'
        },
        'Analysis':     {
            'text': str(
                'In the analysis of a trace services and operations are identified. '
                'The relationships between these services and operations is visualized as graph. '
                'You can see the constructed graph on the left.'
            )},
        'Component':    {
            'text': str(
                'In this context a component is part of the graph that is constructed during the analysis. '
                'One type of component is a node which represents a service of the systems architecture. '
                'Another type of component is an edge which represents an operation of the system.'
            )}
    },
    INTENT_GUIDE_CONTINUE_TEXT:                                [
        'Do you want to know more?',
        'Do you need more infos?',
        'Anything else you want to know?'
    ],
    INTENT_GUIDE_CONTINUE_CONFIRM_TEXT:                        'I am good, let\'s continue! &#x2714;',
    INTENT_GUIDE_OPTION_NAME:                                  'Default-Guide-Option',
    INTENT_GUIDE_CONFIRM_NAME:                                 'Default-Guide-Confirm',

    # Welcome
    INTENT_WELCOME_NAME:                                       'Default-Welcome',
    INTENT_WELCOME_TEXT:                                       str(
        'Hey there! &#x1F44B;<br><br>'
        'I am a chatbot and I will help you to elicit <b>resilience scenarios</b>. '
        'For each scenario we will go through the following steps:<br>'
        '<ol>'
        '<li>Select an <b>architecture</b> to analyze</li>'
        '<li>Select a <b>component</b> of the architecture</li>'
        '<li>Specify a <b>response</b></li>'
        '<li>Specify a <b>response measure</b></li>'
        '<li>Save the <b>resilience scenario</b></li>'
        '</ol>'
        'For every step you can choose from options I propose, you can write to me, '
        'or configure the scenario in the user interface.<br><br>'
        'Everything clear? Are you ready?'
    ),
    INTENT_WELCOME_RESUME_TEXT:                                'Continue where you left. &#x21bb;',
    INTENT_WELCOME_YES_TEXT:                                   'Yes, let\'s go! &#x1F44D;',
    INTENT_WELCOME_NO_TEXT:                                    'No, I need more information. &#x2753;',
    INTENT_WELCOME_CONFIRM_NAME:                               'Default-Welcome-Confirm',
    INTENT_WELCOME_DECLINE_NAME:                               'Default-Welcome-Decline',

    # Elicitation
    INTENT_ELICITATION_ARCHITECTURE_NAME:                      'Elicitation-Select-Architecture',
    INTENT_ELICITATION_ARCHITECTURE_TEXT:                      {
        'title': 'Step 1 - Select an architecture',
        'text':  'Below you are given a list of architectures. Please select one architecture.'
    },
    INTENT_ELICITATION_COMPONENT_NAME:                         'Elicitation-Select-Component',
    INTENT_ELICITATION_COMPONENT_TEXT:                         {
        'title': 'Step 2 - Select a component from <i>{}</i>',
        'text':  'Please select one component from the following selection.'
    },
    INTENT_ELICITATION_COMPONENT_SERVICE_TEXT:                 'Here are the services to choose from ...',
    INTENT_ELICITATION_COMPONENT_OPERATION_TEXT:               'Here are the operations to choose from ...',
    INTENT_ELICITATION_RESPONSE_NAME:                          'Elicitation-Specify-Response',
    INTENT_ELICITATION_RESPONSE_TEXT:                          {
        'title': 'Step 3 - Specify response for <i>{}</i>',
        'text':  'A response is ...'
    },
    INTENT_ELICITATION_RESPONSE_FOLLOWUP_NAME:                 'Elicitation-Specify-Response-Followup',
    INTENT_ELICITATION_RESPONSE_MEASURE_NAME:                  'Elicitation-Specify-Response-Measure',
    INTENT_ELICITATION_RESPONSE_MEASURE_TEXT:                  {
        'title': 'Step 4 - Specify response measure for <i>{}</i>',
        'text':  'A response is ...'
    },
    INTENT_ELICITATION_RESPONSE_MEASURE_FOLLOWUP_NAME:         'Elicitation-Specify-Response-Measure-Followup',
    INTENT_ELICITATION_SAVE_SCENARIO_NAME:                     'Elicitation-Save-Scenario',
    INTENT_ELICITATION_SAVE_SCENARIO_TEXT:                     {
        'title': 'Step 5 - Save scenario',
        'text':  'A response is ...'
    },

    # Util
    INTENT_COMMAND_CONFIG_NAME:                                'Command-Config',
    INTENT_COMMAND_CONFIG_LIST_NAME:                           'Command-Config-List',
    INTENT_COMMAND_MANAGE_NAME:                                'Command-Manage',
    INTENT_COMMAND_MANAGE_LIST_NAME:                           'Command-Manage-List',

    # Extra
    INTENT_FACT_NAME:                                          'Extra-Fact',
    INTENT_FACT_TEXT:                                          [
        'I didn\'t know that one &#x1F446;.',
        'Hm, very interesting.',
        'Who would have thought...'
    ],
    INTENT_JOKE_NAME:                                          'Extra-Joke',
    INTENT_JOKE_TEXT:                                          [
        'Yeah, that\'s a good one &#x1F604;.',
        'Yikes &#x1F923;.',
        'Not so sure about that one &#x1F928;.'
    ]
}
