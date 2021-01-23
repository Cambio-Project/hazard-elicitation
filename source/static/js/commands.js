class Commands {
    static CONFIG_COMMANDS = {
        "set-dark-theme":            "dark-theme",
        "set-sticky-nodes":          "sticky-nodes",
        "set-zoom":                  "graph-zoom",
        "set-node-visibility":       "show-nodes",
        "set-edge-visibility":       "show-edges",
        "set-node-label-visibility": "show-node-labels",
        "set-edge-label-visibility": "show-edge-labels",
    }

    static MANAGE_COMMANDS = {
        "select": Graph.selectElement
    }

    static castValues(values) {
        let casted_values = [];
        for (const el of values) {
            if (el.isBool())
                casted_values.push(el.parseBool());
            else if (el.isNumber())
                casted_values.push(el.parseNumber());
            else
                casted_values.push(el);
        }
        return casted_values;
    }

    constructor() {

    }

    call(action, values) {
        if (action === "command") {
            if (values.length < 1) {
                warn("At least one argument required (command).")
                return;
            }

            const command = values[0];
            let args;

            if (values.length > 1)
                args = Commands.castValues(values.slice(1));


            if (command in Commands.CONFIG_COMMANDS)
                this.configCommand(command, args);
            else if (command in Commands.MANAGE_COMMANDS)
                this.manageCommand(command, args);
            else
                warn("Unknown command '{}'".format(command))
        }
    }

    configCommand(command, args) {
        const el_id = Commands.CONFIG_COMMANDS[command];
        // Use default value if no value was sent.
        // This will use the default for every element in the argument list.
        if(args)
            args = args.map(el => el === "" ? Config.getDefault(el_id) : el);

        Config.setElement(el_id, ...args);
        Config.updateControl(document.getElementById(el_id));
    }

    manageCommand(command, args) {
        Commands.MANAGE_COMMANDS[command](...args);
    }
}
