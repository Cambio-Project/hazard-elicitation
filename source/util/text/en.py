from util.text.ids import *

TEXT = {
    DEFAULT:                          '...',
    INTENT_FALLBACK_NAME:             '0-fallback',
    INTENT_FALLBACK_TEXT:             [
        'That doesn\'t compute. Maybe you can rephrase your sentence?',
        'I don\'t know what you mean. Can you elaborate?',
        'I missed what you said. What was that?',
        'Sorry, could you say that in a different way?',
        'Sorry, I didn\'t get that. Can you rephrase?',
        'Sorry, what was that?',
        'I didn\'t get that. Can you try something different?'
    ],
    INTENT_FALLBACK_GIBBERISH_NAME:   '0-fallback-gibberish',
    INTENT_FALLBACK_GIBBERISH_TEXT:   [
        'That doesn\'t really make sense.',
        'Please write something in proper english.'
    ],
    INTENT_FALLBACK_INSULT_NAME:      '0-fallback-insult',
    INTENT_FALLBACK_INSULT_TEXT:      [
        'Hey that\'s not nice. Please stay professional!',
        'I am sorry if you feel that way, but let\'s stay focused.'
    ],
    INTENT_HELP_NAME:                 '0-help',
    INTENT_HELP_TEXT:                 [
        str('Hang on, help is on it\'s way!'
            'I am a chatbot that helps to elicit resilience scenarios.')
    ],
    INTENT_WELCOME_NAME:              '0-welcome',
    INTENT_WELCOME_TEXT:              [
        'Hi! How are you doing?',
        'Hello! How can I help you?',
        'Good day! What can I do for you?',
        'Greetings! How may I help you?'
    ],
    INTENT_ELICITATION_QUESTION_NAME: '1-elicitation-question',
    INTENT_ELICITATION_QUESTION_TEXT: [
        'Is the service {} essential for the service to run optimally?'
    ],
    INTENT_FACT_NAME:                 'x-fact',
    INTENT_JOKE_NAME:                 'x-joke'
}
