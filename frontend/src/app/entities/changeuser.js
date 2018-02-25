"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * Created by Hanicz on 2/19/2017.
 */
var serializable_1 = require("../utils/serializable");
var ChangeUser = /** @class */ (function (_super) {
    __extends(ChangeUser, _super);
    function ChangeUser() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ChangeUser.prototype.ChangeUser = function () {
        this.new_password = "";
        this.old_password = "";
        this.new_email = "";
    };
    return ChangeUser;
}(serializable_1.Serializable));
exports.ChangeUser = ChangeUser;
//# sourceMappingURL=changeuser.js.map