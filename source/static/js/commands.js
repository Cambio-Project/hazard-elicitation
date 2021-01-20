class Commands {
    static COMMANDS = {
        'set-dark-theme': setDarkTheme,
        'set-sticky-nodes': Graph.stickyNodes,
        'set-zoom': Graph.zoom,
        'set-node-visibility': Graph.showNodes,
        'set-edge-visibility': Graph.showEdges,
        'set-node-label-visibility': Graph.showNodeLabels,
        'set-edge-label-visibility': Graph.showEdgeLabels,
    }

    constructor() {

    }

    call(action, values) {
        if (action === "command") {
            if (values.length < 1) {
                warn("At least one argument required.")
                return;
            }

            const command = values[0];
            const args    = values.slice(1);

            if (!(command in Commands.COMMANDS)) {
                warn("Unknown command '{}'".format(command))
                return;
            }

            if (args.length < 2) {
                warn("At least two argument required for command call.")
            } else if (args.length === 2) {
                const type  = args[0];
                const value = args[1];

                switch (type) {
                    case "bool":
                        Commands.COMMANDS[command](value.parseBool());
                        break;
                    default:
                        warn("Unknown type " + type)
                }
            } else {
                Commands.COMMANDS[command](...values.slice(1));
            }
        }
    }
}
