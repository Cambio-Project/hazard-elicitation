from typing import Dict, List, Any


class IDFResponse:
    def __init__(self, data: Dict = None):
        self._data = data if data else {'type': '', 'payload': {}}

    def __repr__(self) -> Dict:
        return self._data

    @property
    def type(self) -> str:
        return self._data.get('type', '')

    @property
    def payload(self) -> Dict:
        return self._data.get('payload')

    @payload.setter
    def payload(self, payload: Dict):
        self._data['payload'] = payload


class EmptyResponse(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'empty'


class ActionResponse(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'action'
        self._data['payload']['values'] = []

    def __iadd__(self, value):
        self._data['payload']['values'] += value

    @staticmethod
    def create(action: str = '', values: List[Any] = None):
        response = ActionResponse()
        response.action = action
        response.values = values
        return response.__repr__()

    @property
    def action(self) -> str:
        return self._data['payload']['action']

    @action.setter
    def action(self, action: str):
        self._data['payload']['action'] = action

    @property
    def values(self) -> List[Any]:
        return self._data['payload']['values']

    @values.setter
    def values(self, values: List[Any]):
        self._data['payload']['values'] = values


class MultiActionResponse(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'multi_action'
        self._data['payload']['values'] = []

    def __iadd__(self, value):
        self._data['payload']['values'] += value

    @staticmethod
    def create(actions: Dict[str, List]):
        response = MultiActionResponse()
        for action, values in actions.items():
            response.add_action(action, values)
        return response.__repr__()

    @property
    def values(self) -> List[Dict]:
        return self._data['payload']['values']

    @values.setter
    def values(self, values: List[Dict]):
        self._data['payload']['values'] = values

    def add_action(self, action: str, values: List[Any]):
        self._data['payload']['values'].append({
            'action': action,
            'values': values
        })


class FormattingResponse(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'formatting'

    def __iadd__(self, text: str):
        self._data['payload']['text'] += text

    @staticmethod
    def create(text: str = ''):
        response = FormattingResponse()
        response.text = text
        return response.__repr__()

    @property
    def text(self) -> str:
        return self._data['payload']['text']

    @text.setter
    def text(self, text: str):
        self._data['payload']['text'] = text


class TextResponse(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'text'

    def __iadd__(self, text: str):
        self._data['payload']['text'] += text

    @staticmethod
    def create(text: str = ''):
        response = TextResponse()
        response.text = text
        return response.__repr__()

    @property
    def text(self) -> str:
        return self._data['payload']['text']

    @text.setter
    def text(self, text: str):
        self._data['payload']['text'] = text
        

class CardResponse(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'card'

    @staticmethod
    def create(title: str = '', text: str = '', image: str = '', link: Dict[str, str] = None):
        response = CardResponse()
        response.title = title
        response.text = text
        response.image = image
        response.link = link
        return response.__repr__()

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


class QuickReplyResponse(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'quick_reply'
        self._data['payload']['values'] = []

    def __iter__(self):
        return self._data['payload'].get('values', [])

    @staticmethod
    def create(replies: Dict[str, str] = None):
        response = QuickReplyResponse()
        for reply in replies:
            response.add_reply(**reply)
        return response.__repr__()

    @property
    def replies(self) -> List[Dict[str, str]]:
        return self._data['payload']['values']

    @replies.setter
    def replies(self, replies: List[Dict[str, str]]):
        self._data['payload']['values'] = replies

    def add_reply(self, text: str, action: str, values: List):
        self._data['payload']['values'].append({
            'text': text,
            'action': action,
            'values': values
        })


class AccordionResponse(IDFResponse):
    def __init__(self, data: Dict = None):
        super().__init__(data)
        self._data['type'] = 'accordion'
        self._data['payload']['values'] = []

    def __iter__(self):
        return self._data['payload'].get('values', [])

    @staticmethod
    def create(panes: List[Dict[str, str]] = None):
        response = AccordionResponse()
        for pane in panes:
            response.add_pane(**pane)
        return response.__repr__()

    @property
    def panes(self) -> List[Dict[str, str]]:
        return self._data['payload']['values']

    @panes.setter
    def panes(self, panes: List[Dict[str, str]]):
        self._data['payload']['values'] = panes

    def add_pane(self, title: str, text: str):
        self._data['payload']['values'].append({
            'title': title,
            'text': text
        })
