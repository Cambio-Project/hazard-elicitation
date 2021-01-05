## Rich Responses

```python
text = {
    'type':    'text',
    'payload': 'Some text!'
}

quick_reply = {
    'type':    'quick_reply',
    'payload': ['Yes', 'No']
}

card = {
    'type':    'card',
    'payload': {
        'title':   'Hi',
        'message': 'Hi there that is wonderful!',
        'link':    'Yep',
    }
}

accordion = {
    'type':    'accordion',
    'payload': [
        {
            'title':   'Spoiler!',
            'content': 'The cake is a lie!'
        },
        {
            'title':   'Look out!',
            'content': 'nevermind'
        }
    ]
}
```
