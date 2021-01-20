## Rich Responses

```python
generic_response = {
    'intent':  '',
    'type':  '',
    'payload':  {},
}

empty = {
    'intent':  '',
    'type':    'empty',
    'payload': {}
}

action = {
    'intent':  '',
    'type':    'action',
    'payload': {
        'action': 'some-action',
        'values': []
    }
}

text = {
    'intent':  '',
    'type':    'text',
    'payload': {
        'text': 'Some text!'
    }
}

card = {
    'intent':  '',
    'type':    'card',
    'payload': {
        'title': 'Hi',
        'text':  'Hi there that is wonderful!',
        'image':  'www.example.com/image',
        'link':  {
            'text': 'Yep',
            'url':  'www.example.com'
        },
    }
}

quick_reply = {
    'intent':  '',
    'type':    'quick_reply',
    'payload': {
        'values': [
            {
                'text':   'Yes',
                'action': ''
            },
            {
                'text':   'No',
                'action': ''
            }
        ]
    }
}

accordion = {
    'intent':  '',
    'type':    'accordion',
    'payload': {
        'values': [
            {
                'title': 'Spoiler!',
                'text':  'The cake is a lie!'
            },
            {
                'title': 'Look out!',
                'text':  'nevermind'
            }
        ]
    }
}
```
