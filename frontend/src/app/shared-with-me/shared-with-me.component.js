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
var file_service_1 = require("../services/file.service");
var SharedWithMeComponent = /** @class */ (function () {
    function SharedWithMeComponent(fileService) {
        this.fileService = fileService;
        this.fileHidden = true;
        this.responseHidden = true;
    }
    SharedWithMeComponent.prototype.ngOnInit = function () {
        this.get_shared_files();
    };
    SharedWithMeComponent.prototype.onSelectFile = function (file) {
        this.fileHidden = false;
        this.selectedFile = file;
    };
    SharedWithMeComponent.prototype.get_shared_files = function () {
        var _this = this;
        this.fileService.get_shared_with_me_files().subscribe(function (json) {
            console.log(json);
            _this.files = json;
        }, function (error) { return console.error('Error: ' + error); });
    };
    SharedWithMeComponent.prototype.showResponse = function (event) {
        var _this = this;
        this.requestResponse = event;
        this.responseHidden = false;
        setTimeout(function () { return _this.responseHidden = true; }, 2000);
    };
    SharedWithMeComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'shared-with-me',
            templateUrl: './shared-with-me.component.html',
            styleUrls: ['./shared-with-me.component.css']
        }),
        __metadata("design:paramtypes", [file_service_1.FileService])
    ], SharedWithMeComponent);
    return SharedWithMeComponent;
}());
exports.SharedWithMeComponent = SharedWithMeComponent;
//# sourceMappingURL=shared-with-me.component.js.map