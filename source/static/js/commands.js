class Commands {
    static MANAGE_COMMANDS = {
        "reply": Chat.addUserMessage,
        "event": Chat.event,
        "select-architecture": Graph.setGraph,
        "select-element": Graph.selectElement,
        "select-response": function() {},
        "select-response-measure": function() {},
        "save-scenario": Content.saveScenario,
    }

    static castValues(values) {
        let casted_values = [];
        for (const el of values) {
            if (isBool(el))
                casted_values.push(el.parseBool());
            else if (isNumber(el))
                casted_values.push(el.parseNumber());
            else
                casted_values.push(el);
        }
        return casted_values;
    }

    call(action, values) {
        if (action === "command") {
            if (values.length < 1) {
                console.warn("At least one argument required (command).")
                return;
            }

            const command = values[0];
            let args = [];

            if (values.length > 1)
                args = Commands.castValues(values.slice(1));

            console.debug("Call: {}({})".format(command, args.join(",")));


            if (command in Commands.MANAGE_COMMANDS)
                this.manageCommand(command, args);
            else
                console.warn("Unknown command '{}'".format(command))
        }
    }

    manageCommand(command, args) {
        Commands.MANAGE_COMMANDS[command](...args);
    }
}
