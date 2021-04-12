from typing import List, Dict

from google.protobuf.struct_pb2 import ListValue

from dialogflow_backend.dialogflow.intent_handlers.elicitation.component import elicitation_component_handler
from dialogflow_backend.dialogflow.response_types import *
from dialogflow_backend.dialogflow.util import get_context, is_in_context, set_context_parameters
from util.log import error
from util.text.ids import *
from util.text.text import text, random_selection


async def elicitation_stimuli_handler(result) -> List[Dict]:
    try:
        conversation = [FormattingResponse.create('divider')]

        elicitation = get_context('c-elicitation', result)
        config_context = get_context('c-config', result)
        analysis_context = get_context('c-analysis', result)

        if is_in_context('stimulus', config_context):
            stimulus = config_context.parameters['stimulus']
            if isinstance(stimulus, (list, ListValue)):
                stimulus = ' '.join(config_context.parameters['stimulus'])
            else:
                stimulus = config_context.parameters['stimulus']

            return [ActionResponse.create('command', ['event', 'e-specify-stimulus-source', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'stimulus': stimulus
                }
            }]])]

        # Provide the user with stimuli options.
        artifact = elicitation.parameters['artifact'].lower()
        content = text(INTENT_ELICITATION_STIMULUS_TEXT)
        response = CardResponse.create(
            title=content['title'].format(artifact, elicitation.parameters['component']),
            text=content['text'].format(artifact), spoiler=content['spoiler'])
        conversation.append(response)

        stimuli = text(STIMULUS_RESPONSE_TEXTS)[elicitation.parameters['artifact']]['stimuli']

        quick_reply = QuickReplyResponse()
        for option in stimuli:
            quick_reply.add_reply(option, 'event', ['e-specify-stimulus-source', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'stimulus': option
                }}]])
        conversation.append(quick_reply.__repr__())

        return conversation

    except Exception as e:
        error(e)
        return await elicitation_component_handler(result)


async def elicitation_stimuli_followup_handler(result) -> List[Dict]:
    return await elicitation_stimuli_handler(result)


async def elicitation_stimuli_default_handler(result) -> List[Dict]:
    elicitation = get_context('c-elicitation', result)
    if elicitation:
        stimuli = text(STIMULUS_RESPONSE_TEXTS)[elicitation.parameters['artifact']]['stimuli']
        result = set_context_parameters(result, 'c-config', {'stimulus': random_selection(stimuli)})
    return await elicitation_stimuli_handler(result)


async def elicitation_stimuli_source_handler(result) -> List[Dict]:
    try:
        conversation = [FormattingResponse.create('divider')]

        elicitation = get_context('c-elicitation', result)
        config_context = get_context('c-config', result)

        if is_in_context('source', config_context):
            source = config_context.parameters['source']
            if isinstance(source, (list, ListValue)):
                source = ' '.join(config_context.parameters['source'])
            else:
                source = config_context.parameters['source']

            return [ActionResponse.create('command', ['event', 'e-specify-stimulus-environment', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'source': source
                }
            }]])]

        content = text(INTENT_ELICITATION_STIMULUS_SOURCE_TEXT)
        conversation.append(CardResponse.create(
            title=content['title'].format(elicitation.parameters['stimulus']),
            text=content['text'], spoiler=content['spoiler']
        ))

        return conversation

    except Exception as e:
        error(e)
        return await elicitation_component_handler(result)


async def elicitation_stimuli_source_followup_handler(result) -> List[Dict]:
    return await elicitation_stimuli_source_handler(result)


async def elicitation_stimuli_source_default_handler(result) -> List[Dict]:
    elicitation = get_context('c-elicitation', result)
    if elicitation:
        result = set_context_parameters(result, 'c-config', {'source': 'external event'})
    return await elicitation_stimuli_source_handler(result)


async def elicitation_stimuli_environment_handler(result) -> List[Dict]:
    try:
        conversation = [FormattingResponse.create('divider')]

        elicitation = get_context('c-elicitation', result)
        config_context = get_context('c-config', result)

        if is_in_context('environment', config_context):
            environment = config_context.parameters['environment']
            if isinstance(environment, (list, ListValue)):
                environment = ' '.join(config_context.parameters['environment'])
            else:
                environment = config_context.parameters['environment']

            return [ActionResponse.create('command', ['event', 'e-specify-response', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'environment': environment
                }
            }]])]

        content = text(INTENT_ELICITATION_STIMULUS_ENVIRONMENT_TEXT)
        conversation.append(CardResponse.create(
            title=content['title'].format(elicitation.parameters['stimulus']),
            text=content['text'], spoiler=content['spoiler']))

        return conversation

    except Exception as e:
        error(e)
        return await elicitation_component_handler(result)


async def elicitation_stimuli_environment_followup_handler(result) -> List[Dict]:
    return await elicitation_stimuli_environment_handler(result)


async def elicitation_stimuli_environment_default_handler(result) -> List[Dict]:
    elicitation = get_context('c-elicitation', result)
    if elicitation:
        result = set_context_parameters(result, 'c-config', {'environment': 'during normal operation'})
    return await elicitation_stimuli_environment_handler(result)
