from typing import List, Dict

from dialogflow_backend.dialogflow.settings import COMMANDS
from dialogflow_backend.dialogflow.response_types import *

# Config handlers

async def config_handler(result) -> List[Dict]:
    response = ActionResponse()
    response.action = 'command'
    response.values = [
        result.query_result.parameters['config-command'],
        result.query_result.parameters['config-command-value']
    ]
    return [response.__repr__()]


async def config_list_handler(result) -> List[Dict]:
    def code_list(e): return '<{0}><{1}>{2}</{1}></{0}>'.format('li', 'code', e)

    cmd_list = '<ul>{}</ul>'.format(''.join(map(code_list, COMMANDS.keys())))

    response = Accordion()
    response.add_pane('Commands', cmd_list)
    return [response.__repr__()]


async def manage_handler(result) -> List[Dict]:
    response = ActionResponse()
    response.action = 'command'
    response.values = [
        result.query_result.parameters['manage-command'],
        result.query_result.parameters['manage-command-property'],
        result.query_result.parameters['manage-command-value']
    ]
    return [response.__repr__()]
