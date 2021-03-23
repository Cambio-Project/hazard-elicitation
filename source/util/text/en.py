from util.text.ids import *

TEXT = {
    DEFAULT:                                                    '...',

    # Knowledge base
    KB_TEXTS:                                                   [
        {
            'title': 'Tracing',
            'link':  {
                'text': 'Learn more about tracing',
                'url':  'https://en.wikipedia.org/wiki/Tracing_(software)'
            },
            'text':  str(
                'In software engineering, tracing involves a specialized use of logging to record information about a '
                'programs execution. This information is typically used by programmers for debugging purposes; and '
                'additionally, depending on the type and detail of information contained in a trace log, by '
                'experienced system administrators or technical-support personnel and by software monitoring tools to '
                'diagnose common problems with software. Tracing is a cross-cutting concern.')
        },
        {
            'title': 'Jaeger',
            'link':  {
                'text': 'Learn more about jaeger',
                'url':  'https://www.jaegertracing.io/'
            },
            'text':  str(
                'As on-the-ground microservice practitioners are quickly realizing, the majority of operational '
                'problems that arise when moving to a distributed architecture are ultimately grounded in two areas: '
                'networking and observability. It is simply an orders of magnitude larger problem to network and debug '
                'a set of intertwined distributed services versus a single monolithic application.')
        },
        {
            'title': 'Zipkin',
            'link':  {
                'text': 'Learn more about zipkin',
                'url':  'https://zipkin.io/'},
            'text':  str(
                'Zipkin is a distributed tracing system. It helps gather timing data needed to troubleshoot latency '
                'problems in service architectures. Features include both the collection and lookup of this data.')
        }
    ],

    # Stimulus Responses & Response Measures
    STIMULUS_RESPONSE_TEXTS:                                    {
        'Service':   {
            'stimuli':           [
                'Decreased service performance',
                'Service failure'
            ],
            'responses':         [
                'Service should return to normal performance',
                'Service should restart'
            ],
            'response-measures': {
                'normal-time':   ['>10s', '10s', '5s', '3s', '1s', '500ms', '300ms', '100ms', '50ms', '30ms', '10ms',
                                  '<10ms'],
                'normal-cases':  ['99.99%', '99.9%', '99%', '98%', '97%', '96%', '95%'],
                'recovery-time': ['>1h', '1h', '45min', '30min', '15min', '5min', '3min', '1min', '30s', '15s', '10s',
                                  '1s', '<1s']
            }},
        'Operation': {
            'stimuli':           [
                'Spike response times',
                'Response time deviations'
            ],
            'responses':         [
                'Response times should return to normal.'
            ],
            'response-measures': {
                'normal-time':   ['>10s', '10s', '5s', '3s', '1s', '500ms', '300ms', '100ms', '50ms', '30ms', '10ms',
                                  '<10ms'],
                'normal-cases':  ['99.99%', '99.9%', '99%', '98%', '97%', '96%', '95%'],
                'recovery-time': ['5min', '3min', '1min', '30s', '15s', '10s', '1s']
            }},
    },

    # Fallback
    INTENT_PROCESSING_ERROR:                                    'Ops something went wrong.',

    # Default
    INTENT_EMPTY_NAME:                                          'Default-Empty',
    INTENT_CLEAR_NAME:                                          'Default-Clear',
    INTENT_FALLBACK_NAME:                                       'Default-Fallback',
    INTENT_FALLBACK_TEXT:                                       [
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
    INTENT_BYE_NAME:                                            'Default-Bye',
    INTENT_BYE_TEXT:                                            [
        'Nice to work with you! See you around. &#x1F44B;',
        'Okay then! Have a nice day.',
        'Thanks for participating! See you &#x1F44B;'
    ],
    INTENT_HELP_NAME:                                           'Default-Help',
    INTENT_HELP_TEXT:                                           [
        str('Hang on, help is on it\'s way!'
            'I am a chatbot that helps to elicit resilience scenarios.')
    ],

    # Guide
    INTENT_GUIDE_NAME:                                          'Default-Guide',
    INTENT_GUIDE_TEXT:                                          str(
        'Let us go through this, step by step.<br>'
        'Please select or tell me about which topic you would like to learn more about...'),
    INTENT_GUIDE_OPTIONS:                                       {
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
        'Artifact':     {
            'text': str(
                'In this context a artifact is part of the graph that is constructed during the analysis. '
                'One type of artifact is a node which represents a service of the systems architecture. '
                'Another type of artifact is an edge which represents an operation of the system.'
            )}
    },
    INTENT_GUIDE_CONTINUE_TEXT:                                 [
        'Do you want to know more?',
        'Do you need more infos?',
        'Anything else you want to know?'
    ],
    INTENT_GUIDE_CONTINUE_CONFIRM_TEXT:                         'I am good, let\'s continue! &#x2714;',
    INTENT_GUIDE_OPTION_NAME:                                   'Default-Guide-Option',
    INTENT_GUIDE_CONFIRM_NAME:                                  'Default-Guide-Confirm',

    # Welcome
    INTENT_WELCOME_NAME:                                        'Default-Welcome',
    INTENT_WELCOME_TEXT:                                        str(
        'Hey there! &#x1F44B;<br><br>'
        'I am a chatbot and I will help you to elicit <b>resilience scenarios</b>. '
        'For each scenario we will go through the following steps:<br>'
        '<ol>'
        '<li>Select an <b>architecture</b> to analyze</li>'
        '<li>Select a <b>artifact</b> of the architecture</li>'
        '<li>Specify a <b>stimuli</b></li>'
        '<li>Specify a <b>response</b></li>'
        '<li>Specify a <b>response measure</b></li>'
        '<li>Save the <b>resilience scenario</b></li>'
        '</ol>'
        'For every step you can choose from options I propose, you can write to me.<br><br>'
        'Everything clear? Are you ready?'
    ),
    INTENT_WELCOME_RESUME_TEXT:                                 'Continue where you left. &#x21bb;',
    INTENT_WELCOME_YES_TEXT:                                    'Yes, let\'s go! &#x1F44D;',
    INTENT_WELCOME_NO_TEXT:                                     'No, I need more information. &#x2753;',
    INTENT_WELCOME_CONFIRM_NAME:                                'Default-Welcome-Confirm',
    INTENT_WELCOME_DECLINE_NAME:                                'Default-Welcome-Decline',

    # Elicitation
    INTENT_ELICITATION_ARCHITECTURE_NAME:                       'Elicitation-Select-Architecture',
    INTENT_ELICITATION_ARCHITECTURE_TEXT:                       {
        'title': 'Step 1 - Select an architecture',
        'text':  'Below you are given a list of architectures. Please select one architecture.'
    },
    INTENT_ELICITATION_ARCHITECTURE_FOLLOWUP_NAME:              'Elicitation-Select-Architecture-Followup',
    INTENT_ELICITATION_COMPONENT_NAME:                          'Elicitation-Select-Component',
    INTENT_ELICITATION_COMPONENT_TEXT:                          {
        'title': 'Step 2 - Select an artifact from <i>{}</i>',
        'text':  'Please select one artifact from the following selection.'
    },
    INTENT_ELICITATION_COMPONENT_MISSING_TEXT:                  'Try again {} {} is not in the architecture.',
    INTENT_ELICITATION_COMPONENT_SERVICE_TEXT:                  'Here are the <b>services</b> to choose from ...',
    INTENT_ELICITATION_COMPONENT_OPERATION_TEXT:                'Here are the <b>operations</b> to choose from ...',
    INTENT_ELICITATION_COMPONENT_FOLLOWUP_NAME:                 'Elicitation-Select-Component-Followup',
    INTENT_ELICITATION_STIMULUS_NAME:                           'Elicitation-Specify-Stimulus',
    INTENT_ELICITATION_STIMULUS_TEXT:                           {
        'title': 'Step 3 - Specify a stimuli for <i>{}</i>',
        'text':  'What is a potential hazard for this {}?'
    },
    INTENT_ELICITATION_STIMULUS_FOLLOWUP_NAME:                  'Elicitation-Specify-Stimulus-Followup',
    INTENT_ELICITATION_RESPONSE_NAME:                           'Elicitation-Specify-Response',
    INTENT_ELICITATION_RESPONSE_TEXT:                           {
        'title': 'Step 4 - Specify a response for <i>{}</i>',
        'text':  'A response defines what action should be performed against the stimuli.'
    },
    INTENT_ELICITATION_RESPONSE_FOLLOWUP_NAME:                  'Elicitation-Specify-Response-Followup',
    INTENT_ELICITATION_RESPONSE_MEASURE_NAME:                   'Elicitation-Specify-Response-Measure',
    INTENT_ELICITATION_RESPONSE_MEASURE_TEXT:                   {
        'title': 'Step 5 - Specify a response measure for <i>{}</i>',
        'text':  'A response measure quantifies the response.'
    },
    INTENT_ELICITATION_RESPONSE_MEASURE_NORMAL_NAME:            'Elicitation-Specify-Response-Measure-Normal',
    INTENT_ELICITATION_RESPONSE_MEASURE_NORMAL_TEXT:            'What would be an <b>optimal response time</b>?',
    INTENT_ELICITATION_RESPONSE_MEASURE_NORMAL_FOLLOWUP_NAME:   'Elicitation-Specify-Response-Measure-Normal-Followup',
    INTENT_ELICITATION_RESPONSE_MEASURE_CASES_NAME:             'Elicitation-Specify-Response-Measure-Cases',
    INTENT_ELICITATION_RESPONSE_MEASURE_CASES_TEXT:             'In <b>how many cases</b> should this hold?',
    INTENT_ELICITATION_RESPONSE_MEASURE_CASES_FOLLOWUP_NAME:    'Elicitation-Specify-Response-Measure-Cases-Followup',
    INTENT_ELICITATION_RESPONSE_MEASURE_RECOVERY_NAME:          'Elicitation-Specify-Response-Measure-Recovery',
    INTENT_ELICITATION_RESPONSE_MEASURE_RECOVERY_TEXT:          'How long is a <b>non-optimal</b> metric tolerable?',
    INTENT_ELICITATION_RESPONSE_MEASURE_RECOVERY_FOLLOWUP_NAME: 'Elicitation-Specify-Response-Measure-Recovery-Followup',
    INTENT_ELICITATION_SAVE_SCENARIO_NAME:                      'Elicitation-Save-Scenario',
    INTENT_ELICITATION_SAVE_SCENARIO_TEXT:                      {
        'title': 'Step 6 - Save the resilience scenario',
        'text':  'The resilience scenario has now all necessary parameters configured.'
    },
    INTENT_ELICITATION_SUMMARY_SERVICE_MEASURE_TEXT:            str(),
    INTENT_ELICITATION_SUMMARY_OPERATION_MEASURE_TEXT:          str(
        'Normal response time is <b>{}</b> (holds in <b>{}</b> of cases).<br>'
        'Within <b>{}</b> after occurrence of the stimuli the response times return to normal values.'),
    INTENT_ELICITATION_SAVE_SCENARIO_CONTINUE_TEXT:             'Here is the summary of your current scenario.',
    INTENT_ELICITATION_SAVE_SCENARIO_SAVE_TEXT:                 'Is the scenario finished?',
    INTENT_ELICITATION_SAVE_SCENARIO_SAVE_CONFIRM_TEXT:         'Yes, save the scenario. &#x2714;',
    INTENT_ELICITATION_SAVE_SCENARIO_MODIFY_OPTIONS:            {
        'e-select-component':         'Modify the artifact',
        'e-specify-stimuli':          'Modify the stimuli',
        'e-specify-response':         'Modify the response',
        'e-specify-response-measure': 'Modify the response measure'
    },
    INTENT_ELICITATION_SAVE_SCENARIO_CONFIRM_NAME:              'Elicitation-Save-Scenario-Confirm',
    INTENT_ELICITATION_NEXT_STEP_NAME:                          'Elicitation-Next-Step',
    INTENT_ELICITATION_NEXT_STEP_TEXT:                          'Do you want to create another scenario?',
    INTENT_ELICITATION_NEXT_STEP_EXIT_TEXT:                     'No &#x274C;',
    INTENT_ELICITATION_NEXT_STEP_CONTINUE_TEXT:                 'Yes &#x2714;',
    INTENT_ELICITATION_NEXT_STEP_CONFIRM_NAME:                  'Elicitation-Next-Step-Confirm',
    INTENT_ELICITATION_NEXT_STEP_DECLINE_NAME:                  'Elicitation-Next-Step-Decline',

    # Extra
    INTENT_FACT_NAME:                                           'Extra-Fact',
    INTENT_FACT_TEXT:                                           [
        'I didn\'t know that one &#x1F446;.',
        'Hm, very interesting.',
        'Who would have thought...'
    ],
    INTENT_JOKE_NAME:                                           'Extra-Joke',
    INTENT_JOKE_TEXT:                                           [
        'Yeah, that\'s a good one &#x1F604;.',
        'Yikes &#x1F923;.',
        'Not so sure about that one &#x1F928;.'
    ]
}
