"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * Created by Hanicz on 2/19/2017.
 */
var core_1 = require("@angular/core");
require("rxjs/add/operator/toPromise");
var user_service_1 = require("../services/user.service");
var user_1 = require("../utils/user");
var router_1 = require("@angular/router");
var RegisterComponent = /** @class */ (function () {
    function RegisterComponent(userService, router) {
        this.userService = userService;
        this.router = router;
        this.model = new user_1.User();
    }
    RegisterComponent.prototype.register = function () {
        var _this = this;
        this.userService
            .register_user(this.model)
            .subscribe(function (json) {
            _this.model = new user_1.User().fromJSON(json);
            console.log(_this.model.username);
            _this.router.navigate(["/login"]);
        }, function (error) { return console.error('Error: ' + error); });
    };
    RegisterComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'register',
            templateUrl: './register.component.html',
            styleUrls: ['./register.component.css']
        }),
        __metadata("design:paramtypes", [user_service_1.UserService, router_1.Router])
    ], RegisterComponent);
    return RegisterComponent;
}());
exports.RegisterComponent = RegisterComponent;
//# sourceMappingURL=register.component.js.map