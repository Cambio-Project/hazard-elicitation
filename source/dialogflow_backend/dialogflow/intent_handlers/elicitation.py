from typing import List, Dict

from asgiref.sync import sync_to_async

from architecture_extraction_backend.models import ArchitectureModel
from dialogflow_backend.dialogflow.response_types import *
from dialogflow_backend.dialogflow.util import get_context, is_in_context
from util.log import debug
from util.text.text import text
from util.text.ids import *


def fetch_architectures(collection):
    for a in ArchitectureModel.objects.all():
        collection.append(a.name)


# Architecture

async def elicitation_select_architecture_handler(result) -> List[Dict]:
    architectures = []
    await sync_to_async(fetch_architectures)(architectures)

    # Architecture was given as text
    config_context = get_context('c-config', result)
    if is_in_context('arch-file', config_context):

        arch_name = config_context.parameters['arch-file']
        if arch_name in architectures:
            # If architecture name exists, select the matching one.
            return [ActionResponse.create('command', ['select-architecture', arch_name])]

        # Prompt the user to try again.
        return [TextResponse.create('Try again')]

    # Give the user a selection of available architectures.
    divider = FormattingResponse.create('divider')
    content = text(INTENT_ELICITATION_ARCHITECTURE_TEXT)
    question = CardResponse.create(title=content['title'], text=content['text'])

    quick_replies = QuickReplyResponse()
    for arch in architectures:
        quick_replies.add_reply(arch, 'select-architecture', [arch])

    return [divider, question, quick_replies.__repr__()]


async def elicitation_select_architecture_followup_handler(result) -> List[Dict]:
    return await elicitation_select_architecture_handler(result)


# Component

async def elicitation_select_component_handler(result) -> List[Dict]:
    conversation = []

    elicitation = get_context('c-elicitation', result)
    graph_context = get_context('c-graph', result)
    config_context = get_context('c-config', result)

    # Component name was given as text.
    if is_in_context('component-name', config_context):
        component_type = config_context.parameters['component-type']
        component_name = config_context.parameters['component-name']

        # Check against available operations.
        if component_type == 'operation' or component_name in graph_context.parameters['arch']['edges']:
            return [ActionResponse.create('command', ['select-element', 'edge', component_name])]

        # Check against available services.
        elif component_type == 'service' or component_name in graph_context.parameters['arch']['nodes']:
            return [ActionResponse.create('command', ['select-element', 'node', component_name])]

        # Prompt the user to try again.
        return [TextResponse.create('Try again (not in architecture)')]

    # Provide the user with a selection of services and operations.
    conversation.append(FormattingResponse.create('divider'))
    content = text(INTENT_ELICITATION_COMPONENT_TEXT)
    response = CardResponse.create(
        title=content['title'].format(elicitation.parameters['arch']),
        text=content['text'])
    conversation.append(response)

    # Services
    services = TextResponse.create(text(INTENT_ELICITATION_COMPONENT_SERVICE_TEXT))
    service_replies = QuickReplyResponse()

    nodes = sorted(graph_context.parameters['arch']['nodes'], reverse=True)
    for node in nodes:
        service_replies.add_reply(node, 'select-element', ['node', node])

    conversation.append(services)
    conversation.append(service_replies.__repr__())

    # Operations
    operations = TextResponse.create(text(INTENT_ELICITATION_COMPONENT_OPERATION_TEXT))
    operation_replies = QuickReplyResponse()

    edges = sorted(graph_context.parameters['arch']['edges'], reverse=True)
    for edge in edges:
        operation_replies.add_reply(edge, 'select-element', ['edge', edge])

    conversation.append(operations)
    conversation.append(operation_replies.__repr__())

    return conversation


async def elicitation_select_component_followup_handler(result) -> List[Dict]:
    return await elicitation_select_component_handler(result)


# Stimuli

async def elicitation_specify_stimuli_handler(result) -> List[Dict]:
    conversation = []

    elicitation = get_context('c-elicitation', result)

    # Provide the user with stimuli options.
    conversation.append(FormattingResponse.create('divider'))
    artifact = elicitation.parameters['artifact']

    content = text(INTENT_ELICITATION_STIMULUS_TEXT)
    response = CardResponse.create(
        title=content['title'].format(elicitation.parameters['component']),
        text=content['text'].format(artifact.lower()))
    conversation.append(response)

    stimuli = text(STIMULUS_RESPONSE_TEXTS)[elicitation.parameters['artifact']]['stimuli']

    quick_reply = QuickReplyResponse()
    for option in stimuli:
        quick_reply.add_reply(option, 'event', ['e-specify-response', [{
            'name':       'c-elicitation',
            'lifespan':   100,
            'parameters': {
                'stimulus': option
            }}]])
    conversation.append(quick_reply.__repr__())

    return conversation


async def elicitation_specify_stimuli_followup_handler(result) -> List[Dict]:
    return await elicitation_specify_stimuli_handler(result)


# Response

async def elicitation_specify_response_handler(result) -> List[Dict]:
    conversation = []

    elicitation = get_context('c-elicitation', result)
    config_context = get_context('c-config', result)

    # Response was given by quick selection. Proceed to response measure.
    if is_in_context('response', elicitation):
        return await elicitation_specify_response_measure_handler(result)

    # Provide the user with response options
    conversation.append(FormattingResponse.create('divider'))

    content = text(INTENT_ELICITATION_RESPONSE_TEXT)
    response = CardResponse.create(
        title=content['title'].format(elicitation.parameters['component']),
        text=content['text'])
    conversation.append(response)

    responses = text(STIMULUS_RESPONSE_TEXTS)[elicitation.parameters['artifact']]['responses']

    quick_reply = QuickReplyResponse()
    for option in responses:
        quick_reply.add_reply(option, 'event', ['e-specify-response-measure', [{
            'name':       'c-elicitation',
            'lifespan':   100,
            'parameters': {
                'response': option
            }}]])
    conversation.append(quick_reply.__repr__())

    return conversation


async def elicitation_specify_response_followup_handler(result) -> List[Dict]:
    return await elicitation_specify_response_handler(result)


# Response Measure

async def elicitation_specify_response_measure_handler(result) -> List[Dict]:
    conversation = [FormattingResponse.create('divider')]

    elicitation = get_context('c-elicitation', result)
    config_context = get_context('c-config', result)

    artifact = elicitation.parameters['artifact']
    option_selection = text(STIMULUS_RESPONSE_TEXTS)[artifact]['response-measures']

    if is_in_context('times', config_context):
        pass

    # Normal response time is set so we need the probability of the cases.
    if is_in_context('normal-response-time', elicitation) and not is_in_context('normal-cases', elicitation):
        quick_reply = QuickReplyResponse()
        for option in option_selection['normal-cases']:
            quick_reply.add_reply(option, 'event', ['e-specify-response-measure', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'normal-cases': option
                }}]])
        conversation.append(TextResponse.create(text(INTENT_ELICITATION_RESPONSE_MEASURE_NORMAL_CASES_TEXT)))
        conversation.append(quick_reply.__repr__())
        return conversation

    # Probability of the cases is given. Recovery time is needed
    elif is_in_context('normal-cases', elicitation) and not is_in_context('recovery-time', elicitation):
        quick_reply = QuickReplyResponse()
        for option in option_selection['recovery-time']:
            quick_reply.add_reply(option, 'event', ['e-specify-response-measure', [{
                'name':       'c-elicitation',
                'lifespan':   100,
                'parameters': {
                    'recovery-time': option
                }}]])
        conversation.append(TextResponse.create(text(INTENT_ELICITATION_RESPONSE_MEASURE_RECOVERY_TIME_TEXT)))
        conversation.append(quick_reply.__repr__())
        return conversation

    # All response measures are given. Proceed to save scenario.
    elif is_in_context('recovery-time', elicitation):
        return [ActionResponse.create('command', ['event', 'e-save-scenario'])]

    # Provide the user with response options
    content = text(INTENT_ELICITATION_RESPONSE_MEASURE_TEXT)
    response = CardResponse.create(
        title=content['title'].format(elicitation.parameters['component']),
        text=content['text'])
    conversation.append(response)

    quick_reply = QuickReplyResponse()
    for option in option_selection['normal-time']:
        quick_reply.add_reply(option, 'event', ['e-specify-response-measure', [{
            'name':       'c-elicitation',
            'lifespan':   100,
            'parameters': {
                'normal-response-time': option
            }}]])
    conversation.append(TextResponse.create(text(INTENT_ELICITATION_RESPONSE_MEASURE_NORMAL_TIME_TEXT)))
    conversation.append(quick_reply.__repr__())

    return conversation


async def elicitation_specify_response_measure_times_handler(result) -> List[Dict]:
    return await elicitation_specify_response_measure_handler(result)


async def elicitation_specify_response_measure_cases_handler(result) -> List[Dict]:
    return await elicitation_specify_response_measure_handler(result)


# Scenario

def get_scenario(result):
    elicitation = get_context('c-elicitation', result)

    try:
        arch = elicitation.parameters['arch']
        artifact = elicitation.parameters['artifact']
        component = elicitation.parameters['component']
        stimulus = elicitation.parameters['stimulus']
        response = elicitation.parameters['response']
        if artifact == 'Operation':
            measure_time_normal = elicitation.parameters['normal-response-time']
            measure_cases_normal = elicitation.parameters['normal-cases']
            measure_recovery = elicitation.parameters['recovery-time']
            measure = text(INTENT_ELICITATION_SUMMARY_OPERATION_MEASURE_TEXT).format(
                measure_time_normal, measure_cases_normal, measure_recovery)
        else:
            measure_time_normal = elicitation.parameters['normal-response-time']
            measure_cases_normal = elicitation.parameters['normal-cases']
            measure_recovery = elicitation.parameters['recovery-time']
            measure = text(INTENT_ELICITATION_SUMMARY_OPERATION_MEASURE_TEXT).format(  # TODO
                measure_time_normal, measure_cases_normal, measure_recovery)

        return {
            'arch':             arch,
            'component':        component,
            'artifact':         artifact,
            'id':               elicitation.parameters['id'],
            'stimulus':         stimulus,
            'response':         response,
            'response-measure': measure,
        }

    except BaseException as e:
        debug(e)

    return {}


async def elicitation_save_scenario_handler(result) -> List[Dict]:
    conversation = [FormattingResponse.create('divider')]

    content = text(INTENT_ELICITATION_SAVE_SCENARIO_TEXT)
    response = CardResponse.create(title=content['title'], text=content['text'])
    conversation.append(response)

    conversation.append(TextResponse.create(text(INTENT_ELICITATION_SAVE_SCENARIO_CONTINUE_TEXT)))

    scenario = get_scenario(result)
    accordion = AccordionResponse.create([
        {'title': 'Architecture', 'text': scenario['arch']},
        {'title': 'Component', 'text': '{} <b>{}</b>'.format(scenario['artifact'], scenario['component'])},
        {'title': 'Stimulus', 'text': scenario['stimulus']},
        {'title': 'Response', 'text': scenario['response']},
        {'title': 'Response Measure', 'text': scenario['response-measure']}
    ])
    conversation.append(accordion)
    conversation.append(TextResponse.create(text(INTENT_ELICITATION_SAVE_SCENARIO_SAVE_TEXT)))

    quick_replies = QuickReplyResponse()
    for event, option in text(INTENT_ELICITATION_SAVE_SCENARIO_MODIFY_OPTIONS).items():
        quick_replies.add_reply(option, 'event', [event])
    quick_replies.add_reply(text(INTENT_ELICITATION_SAVE_SCENARIO_SAVE_CONFIRM_TEXT), 'save-scenario', [scenario])
    conversation.append(quick_replies.__repr__())

    return conversation


async def elicitation_save_scenario_confirm_handler(result):
    return [ActionResponse.create('command', ['save-scenario', get_scenario(result)])]


async def elicitation_next_step_handler(result):
    conversation = [
        FormattingResponse.create('divider'),
        TextResponse.create(text(INTENT_ELICITATION_NEXT_STEP_TEXT)),
        ActionResponse.create('command', ['event', 'e-clear'])
    ]

    contexts = [{
        'name':       'c-elicitation',
        'lifespan':   100,
        'parameters': {
            'arch': get_context('c-elicitation', result).parameters['arch']
        }
    }, {
        'name':       'c-config',
        'lifespan':   1,
        'parameters': {
            'arch': get_context('c-elicitation', result).parameters['arch']
        }
    }]

    quick_replies = QuickReplyResponse()
    quick_replies.add_reply(text(INTENT_ELICITATION_NEXT_STEP_EXIT_TEXT), 'event', ['e-bye'])
    quick_replies.add_reply(text(INTENT_ELICITATION_NEXT_STEP_CONTINUE_TEXT), 'event', ['e-select-component', contexts])
    conversation.append(quick_replies.__repr__())
    return conversation


async def elicitation_next_step_confirm_handler(result):
    return [ActionResponse.create('command', ['event', 'e-select-component', {
        'name':       'c-elicitation',
        'lifespan':   100,
        'parameters': {
            'arch': get_context('c-config', result).parameters['arch']
        }
    }])]


async def elicitation_next_step_decline_handler(result):
    return [ActionResponse.create('command', ['event', 'e-bye'])]
