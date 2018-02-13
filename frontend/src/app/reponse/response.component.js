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
var ResponseComponent = /** @class */ (function () {
    function ResponseComponent() {
    }
    ResponseComponent.prototype.ngOnChanges = function (changes) {
        for (var propName in changes) {
            if (propName == "inresponse" && this.inresponse != undefined) {
                if (this.inresponse.includes("success")) {
                    this.border = "green";
                    this.background = "#00ff00";
                }
                else if (this.inresponse.includes("fail")) {
                    this.border = "red";
                    this.background = "#ff3300";
                }
            }
        }
    };
    __decorate([
        core_1.Input(),
        __metadata("design:type", String)
    ], ResponseComponent.prototype, "inresponse", void 0);
    ResponseComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'response',
            templateUrl: './response.component.html',
            styleUrls: ['./response.component.css']
        }),
        __metadata("design:paramtypes", [])
    ], ResponseComponent);
    return ResponseComponent;
}());
exports.ResponseComponent = ResponseComponent;
//# sourceMappingURL=response.component.js.map