def next_event(result):
    """
    Helper function to determine which step has to be taken next.
    @param result:  Dialogflow response object
    @return: Name of the event that should be send.
    """
    context = get_context('c-elicitation', result)
    if context:
        if is_in_context('arch', context):
            continue_event = 'e-select-component'
        elif is_in_context('component', context):
            continue_event = 'e-specify-response'
        elif is_in_context('response', context):
            continue_event = 'e-specify-response-measure'
        elif is_in_context('response-measure', context):
            continue_event = 'e-save-scenario'
        else:
            continue_event = 'e-select-architecture'
    else:
        continue_event = 'e-select-architecture'

    return continue_event


def create_context(name: str, lifespan: int, parameters: dict):
    return {
        'name':       name,
        'lifespan':   lifespan,
        'parameters': parameters
    }


def get_context(name, result):
    for context in result.query_result.output_contexts:
        context_name = context.name[context.name.rfind('/') + 1:]
        if context_name == name:
            return context
    return None


def is_in_context(parameter, context):
    return context and parameter in context.parameters and context.parameters[parameter]
