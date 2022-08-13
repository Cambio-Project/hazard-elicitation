from typing import List, Dict

from asgiref.sync import sync_to_async

from software_architecture_extraction.source.extractor.models.study import ScenarioModel
from dialogflow_backend.dialogflow.intent_handlers.elicitation.description import elicitation_description_handler
from dialogflow_backend.dialogflow.response_types import *
from dialogflow_backend.dialogflow.util import get_context, next_event, is_in_context
from hazard_elicitation.settings import COLLECT_STUDY
from util.log import error
from util.text.ids import *
from util.text.text import text


def get_scenario(result):
    elicitation = get_context('c-elicitation', result)

    scenario = {
        'description':      '',
        'arch':             '',
        'artifact':         '',
        'component':        '',
        'id':               '',
        'stimulus':         '',
        'source':           '',
        'environment':      '',
        'response':         '',
        'response-measure': ''
    }
    try:
        artifact = elicitation.parameters['artifact']

        scenario['description'] = elicitation.parameters['description']
        scenario['arch'] = elicitation.parameters['arch']
        scenario['artifact'] = artifact
        scenario['component'] = elicitation.parameters['component']
        scenario['id'] = elicitation.parameters['id']
        scenario['stimulus'] = elicitation.parameters['stimulus']
        scenario['source'] = elicitation.parameters['source']
        scenario['environment'] = elicitation.parameters['environment']
        scenario['response'] = elicitation.parameters['response']
        scenario['measure'] = {}

        if artifact == 'Service':
            measure_cases_normal = elicitation.parameters['normal-cases']
            measure_recovery = elicitation.parameters['recovery-time']
            measure = text(INTENT_ELICITATION_SUMMARY_SERVICE_MEASURE_TEXT).format(
                measure_cases_normal, measure_recovery)
            scenario['measure']['normal-availability'] = elicitation.parameters['normal-cases']
            scenario['measure']['recovery-time'] = elicitation.parameters['recovery-time']
        else:
            measure_time_normal = elicitation.parameters['normal-response-time']
            measure_cases_normal = elicitation.parameters['normal-cases']
            measure_recovery = elicitation.parameters['recovery-time']
            measure = text(INTENT_ELICITATION_SUMMARY_OPERATION_MEASURE_TEXT).format(
                measure_time_normal, measure_cases_normal, measure_recovery)
            scenario['measure']['normal-response-time'] = elicitation.parameters['normal-response-time']
            scenario['measure']['normal-cases'] = elicitation.parameters['normal-cases']
            scenario['measure']['recovery-time'] = elicitation.parameters['recovery-time']

        scenario['response-measure'] = measure

    except ValueError as e:
        error(e)

    return scenario


async def elicitation_save_scenario_handler(result) -> List[Dict]:
    try:
        conversation = [FormattingResponse.create('divider')]

        content = text(INTENT_ELICITATION_SAVE_SCENARIO_TEXT)
        response = CardResponse.create(title=content['title'], text=content['text'])
        conversation.append(response)

        conversation.append(TextResponse.create(text(INTENT_ELICITATION_SAVE_SCENARIO_CONTINUE_TEXT)))

        scenario = get_scenario(result)

        accordion = AccordionResponse.create([
            {'title': 'Description', 'text': '<b>{}</b>'.format(scenario['description'])},
            {'title': 'Artifact', 'text': '{} <b>{}</b>'.format(scenario['artifact'], scenario['component'])},
            {'title': 'Stimulus', 'text': '<b>{}</b> caused by <b>{}</b> (<b>{}</b>)'.format(
                scenario['stimulus'],
                scenario['source'],
                scenario['environment'])},
            {'title': 'Response', 'text': '<b>{}</b>'.format(scenario['response'])},
            {'title': 'Response Measure', 'text': '<b>{}</b>'.format(scenario['response-measure'])}
        ])
        conversation.append(accordion)
        conversation.append(TextResponse.create(text(INTENT_ELICITATION_SAVE_SCENARIO_SAVE_TEXT)))

        quick_replies = QuickReplyResponse()
        for event, option in text(INTENT_ELICITATION_SAVE_SCENARIO_MODIFY_OPTIONS).items():
            quick_replies.add_reply(option, 'event', [event])
        quick_replies.add_reply(text(INTENT_ELICITATION_SAVE_SCENARIO_SAVE_CONFIRM_TEXT), 'save-scenario', [scenario])
        conversation.append(quick_replies.__repr__())

        if COLLECT_STUDY:
            session_name = result.query_result.output_contexts[0].name
            session = session_name[session_name.find('sessions') + 9:session_name.rfind('/contexts')]

            await sync_to_async(ScenarioModel.objects.create)(session_id=session, content=scenario)

        return conversation

    except BaseException as e:
        error(e)
        return [ActionResponse.create('command', ['event', next_event(result)])]


async def elicitation_save_scenario_confirm_handler(result):
    return [ActionResponse.create('command', ['save-scenario', get_scenario(result)])]


async def elicitation_next_step_handler(result):
    try:
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
            'lifespan':   3,
            'parameters': {
                'arch': get_context('c-elicitation', result).parameters['arch']
            }
        }]

        quick_replies = QuickReplyResponse()
        quick_replies.add_reply(text(INTENT_ELICITATION_NEXT_STEP_EXIT_TEXT), 'event', ['e-bye'])
        quick_replies.add_reply(text(INTENT_ELICITATION_NEXT_STEP_CONTINUE_TEXT), 'event',
                                ['e-select-component', contexts])
        conversation.append(quick_replies.__repr__())

        return conversation

    except Exception as e:
        error(e)
        return [ActionResponse.create('command', ['event', next_event(result)])]


async def elicitation_next_step_confirm_handler(result):
    config_context = get_context('c-config', result)
    if is_in_context('arch', config_context):
        return [ActionResponse.create('command', ['event', 'e-select-component', {
            'name':       'c-elicitation',
            'lifespan':   100,
            'parameters': {
                'arch': config_context.parameters['arch']
            }
        }])]
    else:
        return [ActionResponse.create('command', ['event', 'e-select-architecture'])]


async def elicitation_next_step_decline_handler(result):
    return [ActionResponse.create('command', ['event', 'e-bye'])]
