"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Serializable = /** @class */ (function () {
    function Serializable() {
    }
    Serializable.prototype.fromJSON = function (json) {
        for (var propName in json)
            this[propName] = json[propName];
        return this;
    };
    return Serializable;
}());
exports.Serializable = Serializable;
//# sourceMappingURL=serializable.js.map