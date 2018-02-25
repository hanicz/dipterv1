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
var router_1 = require("@angular/router");
var changeuser_1 = require("../entities/changeuser");
var customResponse_1 = require("../utils/customResponse");
var SettingsComponent = /** @class */ (function () {
    function SettingsComponent(userService, router) {
        this.userService = userService;
        this.router = router;
        this.model = new changeuser_1.ChangeUser();
    }
    SettingsComponent.prototype.changeData = function () {
        this.userService
            .changedata(this.model)
            .subscribe(function (json) {
            console.log(new customResponse_1.CustomResponse().fromJSON(json).Response);
        }, function (error) { return console.error('Error: ' + error); });
    };
    SettingsComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'settings',
            templateUrl: './settings.component.html',
            styleUrls: ['./settings.component.css']
        }),
        __metadata("design:paramtypes", [user_service_1.UserService, router_1.Router])
    ], SettingsComponent);
    return SettingsComponent;
}());
exports.SettingsComponent = SettingsComponent;
//# sourceMappingURL=settings.component.js.map