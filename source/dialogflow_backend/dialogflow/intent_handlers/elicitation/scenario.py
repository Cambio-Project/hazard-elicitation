from typing import List, Dict

from asgiref.sync import sync_to_async

from architecture_extraction_backend.models.study import ScenarioModel
from dialogflow_backend.dialogflow.intent_handlers.elicitation.description import elicitation_description_handler
from dialogflow_backend.dialogflow.response_types import FormattingResponse, CardResponse, TextResponse, \
    AccordionResponse, QuickReplyResponse, ActionResponse
from dialogflow_backend.dialogflow.util import get_context
from hazard_elicitation.settings import COLLECT_STUDY
from util.log import error
from util.text.ids import INTENT_ELICITATION_SUMMARY_OPERATION_MEASURE_TEXT, INTENT_ELICITATION_SAVE_SCENARIO_TEXT, \
    INTENT_ELICITATION_SAVE_SCENARIO_CONTINUE_TEXT, INTENT_ELICITATION_SAVE_SCENARIO_SAVE_TEXT, \
    INTENT_ELICITATION_SAVE_SCENARIO_MODIFY_OPTIONS, INTENT_ELICITATION_SAVE_SCENARIO_SAVE_CONFIRM_TEXT, \
    INTENT_ELICITATION_NEXT_STEP_TEXT, INTENT_ELICITATION_NEXT_STEP_EXIT_TEXT, \
    INTENT_ELICITATION_NEXT_STEP_CONTINUE_TEXT
from util.text.text import text


def get_scenario(result):
    elicitation = get_context('c-elicitation', result)

    try:
        description = elicitation.parameters['description']
        arch = elicitation.parameters['arch']
        artifact = elicitation.parameters['artifact']
        component = elicitation.parameters['component']
        stimulus = elicitation.parameters['stimulus']
        source = elicitation.parameters['source']
        environment = elicitation.parameters['environment']
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
            'description':      description,
            'arch':             arch,
            'component':        component,
            'artifact':         artifact,
            'id':               elicitation.parameters['id'],
            'stimulus':         stimulus,
            'source':           source,
            'environment':      environment,
            'response':         response,
            'response-measure': measure,
        }

    except BaseException as e:
        error(e)

    return {}


async def elicitation_save_scenario_handler(result) -> List[Dict]:
    try:
        conversation = [FormattingResponse.create('divider')]

        content = text(INTENT_ELICITATION_SAVE_SCENARIO_TEXT)
        response = CardResponse.create(title=content['title'], text=content['text'])
        conversation.append(response)

        conversation.append(TextResponse.create(text(INTENT_ELICITATION_SAVE_SCENARIO_CONTINUE_TEXT)))

        scenario = get_scenario(result)
        accordion = AccordionResponse.create([
            {'title': 'Description', 'text': scenario['description']},
            {'title': 'Artifact', 'text': '{} <b>{}</b>'.format(scenario['artifact'], scenario['component'])},
            {'title': 'Stimulus', 'text': '<i>{}</i> caused by <i>{}</i> (<i>{}</i>)'.format(
                scenario['stimulus'],
                scenario['source'],
                scenario['environment'])},
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

        if COLLECT_STUDY:
            session_name = result.query_result.output_contexts[0].name
            session = session_name[session_name.find('sessions') + 9:session_name.rfind('/contexts')]

            await sync_to_async(ScenarioModel.objects.create)(session_id=session, content=scenario)

        return conversation

    except Exception as e:
        error(e)
        return await elicitation_description_handler(result)


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