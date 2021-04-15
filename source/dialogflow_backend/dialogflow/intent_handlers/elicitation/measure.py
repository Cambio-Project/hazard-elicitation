from typing import List, Dict

from dialogflow_backend.dialogflow.intent_handlers.elicitation.response import elicitation_response_handler
from dialogflow_backend.dialogflow.response_types import FormattingResponse, CardResponse, ActionResponse, \
    QuickReplyResponse, TextResponse
from dialogflow_backend.dialogflow.util import get_context, is_in_context, set_context_parameters, next_event
from util.log import error
from util.text.ids import *
from util.text.text import text, random_selection


async def elicitation_measure_handler(result) -> List[Dict]:
    try:
        conversation = [FormattingResponse.create('divider')]

        elicitation = get_context('c-elicitation', result)

        # Provide the user with response time options.
        content = text(INTENT_ELICITATION_MEASURE_TEXT)
        response = CardResponse.create(
            title=content['title'].format(elicitation.parameters['component']),
            text=content['text'])
        conversation.append(response)

        artifact = elicitation.parameters['artifact']
        if artifact == 'Operation':
            conversation.append(ActionResponse.create('command', ['event', 'e-specify-response-measure-normal']))
        else:
            conversation.append(ActionResponse.create('command', ['event', 'e-specify-response-measure-cases']))
        return conversation

    except Exception as e:
        error(e)
        return await elicitation_response_handler(result)


async def elicitation_measure_normal_handler(result) -> List[Dict]:
    try:
        conversation = [FormattingResponse.create('divider')]
        elicitation = get_context('c-elicitation', result)
        config_context = get_context('c-config', result)
        artifact = elicitation.parameters['artifact']
        options = text(STIMULUS_RESPONSE_TEXTS)[artifact]['response-measures']['normal-time']

        # Normal response time is set.
        if is_in_context('normal-response-time', config_context):
            amount = config_context.parameters['normal-response-time']['amount']
            unit = config_context.parameters['normal-response-time']['unit']
            return [ActionResponse.create('command', ['event', next_event(result), [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'normal-response-time': f'{amount} {unit}'
                }
            }]])]
        elif is_in_context('duration', config_context):
            return [ActionResponse.create('command', ['event', next_event(result), [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'normal-response-time': config_context.parameters['duration']
                }
            }]])]

        # Cases quick responses.
        quick_reply = QuickReplyResponse()
        for option in options:
            quick_reply.add_reply(option, 'event', ['e-specify-response-measure-cases', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'normal-response-time': option
                }}]])
        conversation.append(TextResponse.create(text(INTENT_ELICITATION_MEASURE_NORMAL_TEXT)))
        conversation.append(quick_reply.__repr__())
        return conversation

    except Exception as e:
        error(e)
        return await elicitation_response_handler(result)


async def elicitation_measure_normal_followup_handler(result) -> List[Dict]:
    return await elicitation_measure_normal_handler(result)


async def elicitation_measure_normal_default_handler(result) -> List[Dict]:
    elicitation = get_context('c-elicitation', result)
    if elicitation:
        result = set_context_parameters(result, 'c-config', {
            'normal-response-time': {
                'amount': '100',
                'unit':   'ms'
            }})
    return await elicitation_measure_normal_handler(result)


async def elicitation_measure_cases_handler(result) -> List[Dict]:
    try:
        conversation = [FormattingResponse.create('divider')]
        elicitation = get_context('c-elicitation', result)
        config_context = get_context('c-config', result)
        artifact = elicitation.parameters['artifact']
        options = text(STIMULUS_RESPONSE_TEXTS)[artifact]['response-measures']['normal-cases']

        # Probability of the cases is given.
        if is_in_context('normal-cases', config_context):
            cases = config_context.parameters['normal-cases']
            percent = '%' if '%' not in cases else ''
            return [ActionResponse.create('command', ['event', next_event(result), [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'normal-cases': f'{cases}{percent}'
                }
            }]])]

        # Recovery time quick responses
        quick_reply = QuickReplyResponse()
        for option in options:
            quick_reply.add_reply(option, 'event', ['e-specify-response-measure-recovery', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'normal-cases': option
                }}]])
        if artifact == 'Service':
            conversation.append(TextResponse.create(text(INTENT_ELICITATION_MEASURE_CASES_SERVICE_TEXT)))
        else:
            conversation.append(TextResponse.create(text(INTENT_ELICITATION_MEASURE_CASES_OPERATION_TEXT)))
        conversation.append(quick_reply.__repr__())
        return conversation

    except Exception as e:
        error(e)
        return await elicitation_response_handler(result)


async def elicitation_measure_cases_followup_handler(result) -> List[Dict]:
    return await elicitation_measure_cases_handler(result)


async def elicitation_measure_cases_default_handler(result) -> List[Dict]:
    elicitation = get_context('c-elicitation', result)
    if elicitation:
        artifact = elicitation.parameters['artifact']
        options = text(STIMULUS_RESPONSE_TEXTS)[artifact]['response-measures']['normal-cases']
        result = set_context_parameters(result, 'c-config', {'normal-cases': random_selection(options)})
    return await elicitation_measure_cases_handler(result)


async def elicitation_measure_recovery_handler(result) -> List[Dict]:
    try:
        conversation = [FormattingResponse.create('divider')]
        elicitation = get_context('c-elicitation', result)
        config_context = get_context('c-config', result)
        artifact = elicitation.parameters['artifact']
        options = text(STIMULUS_RESPONSE_TEXTS)[artifact]['response-measures']['recovery-time']

        # Recovery time is given.
        if is_in_context('recovery-time', config_context):
            amount = config_context.parameters['recovery-time']['amount']
            unit = config_context.parameters['recovery-time']['unit']
            return [ActionResponse.create('command', ['event', next_event(result), [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'recovery-time': f'{amount} {unit}'
                }
            }]])]

        # Recovery time quick responses
        quick_reply = QuickReplyResponse()
        for option in options:
            quick_reply.add_reply(option, 'event', ['e-specify-description', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'recovery-time': option
                }}]])
        conversation.append(TextResponse.create(text(INTENT_ELICITATION_MEASURE_RECOVERY_TEXT)))
        conversation.append(quick_reply.__repr__())
        return conversation

    except Exception as e:
        error(e)
        return await elicitation_response_handler(result)


async def elicitation_measure_recovery_followup_handler(result) -> List[Dict]:
    return await elicitation_measure_recovery_handler(result)


async def elicitation_measure_recovery_default_handler(result) -> List[Dict]:
    elicitation = get_context('c-elicitation', result)
    if elicitation:
        result = set_context_parameters(result, 'c-config', {'recovery-time': {
            'amount': '10',
            'unit':   'minutes'
        }})
    return await elicitation_measure_recovery_handler(result)
