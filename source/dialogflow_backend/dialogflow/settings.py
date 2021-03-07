INTENTS = [
    'Command-Config',
    'Command-Config-List',
    'Command-Manage',
    'Default-Fallback',
    'Default-Help',
    'Default-Welcome',
    'Default-Welcome-Confirm',
    'Default-Welcome-Decline',
    'Elicitation-Select-Architecture',
    'Elicitation-Select-Component',
    'Elicitation-Specify-Response',
    'Extra-Fact',
    'Extra-Joke',
    'Guide'
]

ENTITIES = [
    'boolean',
    'command',
    'command-regex',
    'command-value',
    'config-command',
    'config-command-synonyms',
    'guide-option',
    'manage-command',
    'manage-command-property',
    'manage-command-synonyms',
    'manage-command-value',
    'string',
    'string-camel',
    'string-capital'
]

CONTEXTS = [
    'c-config',
    'c-elicitation',
    'c-guide',
    'c-guide-option',
    'c-manage',
    'c-welcome',
]

COMMANDS = {
    'set-dark-theme':            0,
    'set-sticky-nodes':          0,
    'set-zoom':                  0,
    'set-node-visibility':       0,
    'set-edge-visibility':       0,
    'set-node-label-visibility': 0,
    'set-edge-label-visibility': 0,
}
