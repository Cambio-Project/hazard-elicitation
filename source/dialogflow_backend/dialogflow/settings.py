INTENTS = [
    'Command-Config',
    'Command-Config-List',
    'Command-Manage',
    'Default-Fallback',
    'Default-Help',
    'Default-Welcome',
    'Elicitation-Question',
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
    'manage-command',
    'manage-command-property',
    'manage-command-synonyms',
    'manage-command-value',
    'string',
    'string-camel',
    'string-capital'
]

CONTEXTS = [
    'guide',
    'elicitation'
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
