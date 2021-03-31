def next_event(result):
    """
    Helper function to determine which step has to be taken next.
    @param result:  Dialogflow response object
    @return: Name of the event that should be send.
    """
    context = get_context('c-elicitation', result)
    if context:
        if is_in_context('description', context):
            continue_event = 'e-save-scenario'
        elif is_in_context('response-measure', context):
            continue_event = 'e-specify-description'
        elif is_in_context('response', context):
            continue_event = 'e-specify-response-measure'
        elif is_in_context('stimulus', context):
            continue_event = 'e-specify-response'
        elif is_in_context('artifact', context):
            continue_event = 'e-specify-stimulus'
        elif is_in_context('arch', context):
            continue_event = 'e-select-component'
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


def set_context_parameters(result, context_name, parameters):
    for index, context in enumerate(result.query_result.output_contexts):
        if context.name.endswith(context_name):
            for key, value in parameters.items():
                result.query_result.output_contexts[index].parameters[key] = value

    return result
