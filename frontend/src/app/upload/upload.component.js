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
var customResponse_1 = require("../utils/customResponse");
var UploadComponent = /** @class */ (function () {
    function UploadComponent(fileService) {
        this.fileService = fileService;
        this.closeEvent = new core_1.EventEmitter();
    }
    UploadComponent.prototype.upload = function () {
        var _this = this;
        this.fileService.upload_file(this.file, this.folder).subscribe(function (json) {
            _this.custResp = new customResponse_1.CustomResponse().fromJSON(json);
            console.log(_this.custResp.Response);
            _this.filePicker.nativeElement.value = "";
            _this.closeEvent.emit();
        }, function (error) { return console.error('Error: ' + error); });
    };
    UploadComponent.prototype.onChange = function (event) {
        this.file = event.srcElement.files;
    };
    UploadComponent.prototype.close = function () {
        this.closeEvent.emit();
    };
    __decorate([
        core_1.Input(),
        __metadata("design:type", Number)
    ], UploadComponent.prototype, "folder", void 0);
    __decorate([
        core_1.Output(),
        __metadata("design:type", Object)
    ], UploadComponent.prototype, "closeEvent", void 0);
    __decorate([
        core_1.ViewChild('filePicker'),
        __metadata("design:type", Object)
    ], UploadComponent.prototype, "filePicker", void 0);
    UploadComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'upload',
            templateUrl: './upload.component.html',
            styleUrls: ['./upload.component.css']
        }),
        __metadata("design:paramtypes", [file_service_1.FileService])
    ], UploadComponent);
    return UploadComponent;
}());
exports.UploadComponent = UploadComponent;
//# sourceMappingURL=upload.component.js.map