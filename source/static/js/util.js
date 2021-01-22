/*
 * Prototypes
 */
String.prototype.format = function () {
    let i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != "undefined" ? args[i++] : "";
    });
};

String.prototype.parseBool = function () {
    return !/(f(alse)|n(o)|o(ff)|0)/.test(this.toLowerCase());
}

Number.prototype.isInteger = function () {
    return Number.isInteger(this);
}

Object.defineProperty(Object.prototype, '_keys', {
    value:      function () { return Object.keys(this); },
    enumerable: false
});

Object.defineProperty(Object.prototype, '_values', {
    value:      function () { return Object.keys(this).map(k => this[k]); },
    enumerable: false
});

Object.defineProperty(Object.prototype, '_entries', {
    value:      function () { return Object.entries(this); },
    enumerable: false
});

Object.defineProperty(Object.prototype, '_empty', {
    value:      function () { return Object.keys(this).length === 0; },
    enumerable: false
});

function isString(what) { return typeof what === "string"; }

function isObject(what) { return typeof what === "object"; }

function isBool(what) { return typeof what === "boolean"; }

function isNumber(what) { return typeof what === "number"; }

/*
 * Config class stores local configuration.
 */
class Config {
    static SETTINGS = {
        "dark-theme":       {default: false, callback: setDarkTheme},
        "graph-zoom":       {default: 1, callback: Graph.zoom},
        "graph-selection":  {default: "", callback: null},
        "sticky-nodes":     {default: false, callback: Graph.stickyNodes},
        "use-tooltips":     {default: false, callback: Graph.useTooltip},
        "show-nodes":       {default: true, callback: Graph.showNodes},
        "show-edges":       {default: true, callback: Graph.showEdges},
        "show-node-labels": {default: true, callback: Graph.showNodeLabels},
        "show-edge-labels": {default: false, callback: Graph.showEdgeLabels}
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

    static setConfig(element) {
        if (Config.SETTINGS[element.id].callback) {
            Config.SETTINGS[element.id].callback(Config.getElement(element.id));
        }
    }

    static getDefault(key) {
        return Config.SETTINGS[key].default;
    }

    static setStorage(key, value) {
        if (isBool(value))
            localStorage.setItem(key, value ? "true" : "false")
        else
            localStorage.setItem(key, value)
    }

    static getStorage(key) {
        const val = localStorage.getItem(key);
        if (val === "true" || val === "false")
            return val.parseBool();
        else
            return val;
    }

    static getElement(id) {
        const el  = $("#" + id);
        const val = el.val();
        if (val === "on") {
            return el.prop("checked");
        }
        return val;
    }

    static setElement(id, val) {
        if(isBool(val))
            $("#" + id).prop("checked", val);
        else
            $("#" + id).val(val);
    }

    static storeConfig() {
        for (const key of Config.SETTINGS._keys()) {
            Config.setStorage(key, Config.getElement(key));
        }
    }

    static loadConfig() {
        for (const key of Config.SETTINGS._keys()) {
            const val = Config.getStorage(key);
            if (val !== null)
                Config.setElement(key, val);
            else
                Config.setElement(key, Config.getDefault(key));

            Config.setConfig(document.getElementById(key));
        }
    }

    /* Properties setter */
    setDarkTheme(value) { document.documentElement.className = value ? "dark-theme" : "light-theme"; }

    showAdvancedElements(show) { const elements = $(".advanced").css("display", show ? "inline-block" : "none"); }
}
