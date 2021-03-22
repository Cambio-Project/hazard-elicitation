/*
 * Prototypes
 */
String.prototype.format = function () {
    let i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != "undefined" ? args[i++] : "";
    });
};

String.prototype.isNumber = function () {
    return isNumber(this);
}

String.prototype.parseNumber = function () {
    return parseFloat(this);
}

String.prototype.isBool = function () {
    return /^(f(alse)|t(rue)|n(o)|y(es)|o(n|ff)|0|1)$/.test(this.toLowerCase());
}

String.prototype.parseBool = function () {
    return !/^(f(alse)|n(o)|o(ff)|0)$/.test(this.toLowerCase());
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

Object.defineProperty(Object.prototype, '_copy', {
    value:      function () { return Object.assign({}, this); },
    enumerable: false
});

function isString(what) { return typeof what === "string"; }

function isObject(what) { return typeof what === "object"; }

function isBool(what) { return typeof what === "boolean"; }

function isNumber(what) { return typeof what === "number"; }

function download(content, fileName, contentType) {
    const a    = document.createElement("a");
    const file = new Blob([content], {type: contentType});
    a.href     = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}
