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
 * Created by Hanicz on 2/21/2017.
 */
var core_1 = require("@angular/core");
var router_1 = require("@angular/router");
require("rxjs/add/operator/switchMap");
var user_service_1 = require("../services/user.service");
var customResponse_1 = require("../utils/customResponse");
var ActivateComponent = /** @class */ (function () {
    function ActivateComponent(userService, route) {
        this.userService = userService;
        this.route = route;
        this.custResp = new customResponse_1.CustomResponse();
    }
    ActivateComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.route.params
            .switchMap(function (params) { return _this.userService.activate_user(params['token']); })
            .subscribe(function (json) {
            _this.custResp = new customResponse_1.CustomResponse().fromJSON(json);
            console.log(_this.custResp.Response);
        }, function (error) { _this.custResp.Response = 'Activation failed'; });
    };
    ActivateComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'activate',
            templateUrl: './activate.component.html',
            styleUrls: ['./activate.component.css']
        }),
        __metadata("design:paramtypes", [user_service_1.UserService,
            router_1.ActivatedRoute])
    ], ActivateComponent);
    return ActivateComponent;
}());
exports.ActivateComponent = ActivateComponent;
//# sourceMappingURL=activate.component.js.map