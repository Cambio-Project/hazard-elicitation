/*
 * Config class stores local configuration.
 */
class Config {
    static SETTINGS = {
        "dark-theme":        {default: false, callback: Config.setDarkTheme},
        "graph-selection":   {default: "", callback: Config.setGraph},
        "sticky-nodes":      {default: false, callback: Config.stickyNodes},
        "curvy-edges":       {default: false, callback: Config.curvyEdges},
        "use-tooltips":      {default: false, callback: Config.useTooltip},
        "use-page-tooltips": {default: true, callback: Config.usePageTooltip},
        "show-nodes":        {default: true, callback: Config.showNodes},
        "show-edges":        {default: true, callback: Config.showEdges},
        "show-node-labels":  {default: true, callback: Config.showNodeLabels},
        "show-edge-labels":  {default: false, callback: Config.showEdgeLabels},
        "graph-zoom":        {default: 1, callback: Config.zoom},
    }

    static print() {
        for (const [k, v] of Config.SETTINGS._entries()) {
            console.log(k, v)
        }
    }

    static printSt() {
        let element = localStorage.length;
        while (element--) {
            console.log(localStorage.key(element), localStorage.getItem(localStorage.key(element)));
        }
    }

    static clear() {
        let element = localStorage.length;
        while (element--) {
            localStorage.removeItem(localStorage.key(element));
        }
    }

    /* Returns a default value. */
    static getDefault(key) {
        return Config.SETTINGS[key].default;
    }

    /* Sets a value to the storage. */
    static setStorage(key, value) {
        if (value !== null) {
            if (isBool(value))
                localStorage.setItem(key, value ? "true" : "false");
            else
                localStorage.setItem(key, value);
        }
    }

    /* Gets a value from the storage. */
    static getStorage(key) {
        const val = localStorage.getItem(key);
        if (val === "true" || val === "false")
            return val.parseBool();
        else
            return val;
    }

    /* Called when a control changes its value. Calls callback with the new value. */
    static updateControl(element) {
        if (element && Config.SETTINGS[element.id].callback) {
            const new_val = Config.getElement(element.id);
            Config.SETTINGS[element.id].callback(new_val);
            Config.setStorage(element.id, new_val);
        }
    }

    /* Returns the value of a control element. */
    static getElement(id) {
        const el  = $("#" + id);
        const val = el.val();

        if (val === "on")
            return el.prop("checked");
        return val;
    }

    /* Sets the value of a control element. */
    static setElement(id, val) {
        let el = $("#" + id);
        if (isBool(val))
            el.prop("checked", val).change();
        else
            el.val(val).change();
    }

    /* Saves all control values to the storage. */
    static storeConfig() {
        for (const key of Config.SETTINGS._keys()) {
            Config.setStorage(key, Config.getElement(key));
        }
    }

    /* Initializes control values from storage or default value and applies the value to the control. */
    static loadConfig() {
        for (const key of Config.SETTINGS._keys()) {
            const val = Config.getStorage(key);
            if (val === null)
                Config.setElement(key, Config.getDefault(key));
            else
                Config.setElement(key, val);

            Config.updateControl(document.getElementById(key));
        }
    }

    /* Properties setter */
    static setDarkTheme(value) { document.documentElement.className = value ? "dark-theme" : "light-theme"; }

    static showAdvancedElements(show) { $(".advanced").css("display", show ? "inline-block" : "none"); }

    static setGraph(name) { if (name) Graph.setGraph(name); }

    static stickyNodes(sticky) { Graph.set("sticky", sticky); }

    static curvyEdges(curvy) { Graph.set("curved_edges", curvy); }

    static showNodes(show) { Graph.this.nodes.style("visibility", show ? "visible" : "hidden"); }

    static showEdges(show) { Graph.this.edges.style("visibility", show ? "visible" : "hidden"); }

    static showNodeLabels(show) { Graph.this.node_labels.style("visibility", show ? "visible" : "hidden"); }

    static showEdgeLabels(show) { Graph.this.edge_labels.style("visibility", show ? "visible" : "hidden"); }

    static useTooltip(use) { Graph.set("tooltip", use); }

    static usePageTooltip(use) { $('[data-toggle="tooltip"]').tooltip(use ? "enable" : "disable"); }

    static zoom(zoom) { Graph.zoom(zoom); }
}
