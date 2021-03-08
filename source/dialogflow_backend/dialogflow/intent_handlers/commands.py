from typing import List, Dict

from dialogflow_backend.dialogflow.data import COMMANDS
from dialogflow_backend.dialogflow.response_types import *


# Config handlers

async def config_handler(result) -> List[Dict]:
    response = ActionResponse.create('command', [
        result.query_result.parameters['config-command'],
        result.query_result.parameters['config-command-value']
    ])
    return [response]


async def config_list_handler(result) -> List[Dict]:
    def code_list(e): return '<{0}><{1}>{2}</{1}></{0}>'.format('li', 'code', e)

    response = AccordionResponse.create([{
        'title': 'Commands',
        'text':  '<ul>{}</ul>'.format(''.join(map(code_list, COMMANDS.keys())))
    }])
    return [response]


async def manage_handler(result) -> List[Dict]:
    response = ActionResponse.create('command', [
        result.query_result.parameters['manage-command'],
        result.query_result.parameters['manage-command-property'],
        result.query_result.parameters['manage-command-value']
    ])
    return [response]
