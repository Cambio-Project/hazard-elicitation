## Rich Responses

```python
generic_response = {
    'type':    '',
    'payload': {},
}

empty = {
    'type':    'empty',
    'payload': {}
}

action = {
    'type':    'action',
    'payload': {
        'action': 'some-action',
        'values': []
    }
}

multi_action = {
    'type':    'action',
    'payload': {
        'values': [{
            'action': 'some-action',
            'values': ['param-1']
        }, {
            'action': 'some-other-action',
            'values': ['param-1', 'param-2']
        }]
    }
}

formatting = {
    'type':    'formatting',
    'payload': {
        'text': 'format specific content'
    }
}

text = {
    'type':    'text',
    'payload': {
        'text': 'Some text!'
    }
}

card = {
    'type':    'card',
    'payload': {
        'title': 'Hi',
        'text':  'Hi there that is wonderful!',
        'image': 'www.example.com/image',
        'link':  {
            'text': 'Yep',
            'url':  'www.example.com'
        },
    }
}

quick_reply = {
    'type':    'quick_reply',
    'payload': {
        'values': [
            {
                'text':   'Yes',
                'action': '',
                'values': []
            },
            {
                'text':   'No',
                'action': '',
                'values': []
            }
        ]
    }
}

accordion = {
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
