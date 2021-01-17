from typing import Dict, Union, List


class IDFResponse:
    def __init__(self, data: Dict = None):
        self._data = data if data else {'intent': '', 'type': '', 'payload': {}}

    def __repr__(self) -> Dict:
        return self._data

    @property
    def intent(self) -> str:
        return self._data.get('intent', '')

    @intent.setter
    def intent(self, intent: str):
        self._data['intent'] = intent

    @property
    def type(self) -> str:
        return self._data.get('type', '')

    @property
    def payload(self) -> Dict:
        return self._data.get('payload')

    @payload.setter
    def payload(self, payload: Dict):
        self._data['payload'] = payload


class TextMessage(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'text'

    def __iadd__(self, text: str):
        self._data['payload']['text'] += text

    @property
    def text(self) -> str:
        return self._data['payload']['text']

    @text.setter
    def text(self, text: str):
        self._data['payload']['text'] = text
        

class Card(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'card'

    @property
    def title(self) -> str:
        return self._data['payload']['title']

    @title.setter
    def title(self, title: str):
        self._data['payload']['title'] = title
    
    @property
    def text(self) -> str:
        return self._data['payload']['text']

    @text.setter
    def text(self, text: str):
        self._data['payload']['text'] = text

    @property
    def image(self) -> str:
        return self._data['payload']['image']

    @image.setter
    def image(self, image: str):
        self._data['payload']['image'] = image

    @property
    def link(self) -> Dict[str, str]:
        return self._data['payload']['link']

    @link.setter
    def link(self, link: Dict[str, str]):
        self._data['payload']['link'] = link


class QuickReply(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'quick_reply'
        self._data['payload']['entries'] = []

    def __iter__(self):
        return self._data['payload'].get('entries', [])

    @property
    def replies(self) -> List[Dict[str, str]]:
        return self._data['payload']['entries']

    @replies.setter
    def replies(self, replies: List[Dict[str, str]]):
        self._data['payload']['entries'] = replies

    def add_reply(self, text: str, action: str):
        self._data['payload']['entries'].append({
            'text': text,
            'action': action
        })


class Accordion(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'accordion'
        self._data['payload']['entries'] = []

    def __iter__(self):
        return self._data['payload'].get('entries', [])

    @property
    def panes(self) -> List[Dict[str, str]]:
        return self._data['payload']['entries']

    @panes.setter
    def panes(self, panes: List[Dict[str, str]]):
        self._data['payload']['entries'] = panes

    def add_pane(self, title: str, text: str):
        self._data['payload']['entries'].append({
            'title': title,
            'text': text
        })
