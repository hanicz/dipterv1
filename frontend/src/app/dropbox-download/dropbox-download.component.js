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
var folder_1 = require("../entities/folder");
var dropbox_service_1 = require("../services/dropbox.service");
var DropboxDownloadComponent = /** @class */ (function () {
    function DropboxDownloadComponent(dropboxService) {
        this.dropboxService = dropboxService;
        this.closeEvent = new core_1.EventEmitter();
        this.downloadEvent = new core_1.EventEmitter();
        this.path = "/";
    }
    DropboxDownloadComponent.prototype.download = function () {
        var _this = this;
        this.dropboxService.download_from_dropbox(this.path, this.filename, this.folder.id).subscribe(function (json) {
            console.log(json);
            _this.path = "/";
            _this.filename = "";
            _this.downloadEvent.emit("File download started successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.downloadEvent.emit("File download failed");
        });
    };
    DropboxDownloadComponent.prototype.close = function () {
        this.closeEvent.emit();
    };
    __decorate([
        core_1.Input(),
        __metadata("design:type", folder_1.Folder)
    ], DropboxDownloadComponent.prototype, "folder", void 0);
    __decorate([
        core_1.Output(),
        __metadata("design:type", Object)
    ], DropboxDownloadComponent.prototype, "closeEvent", void 0);
    __decorate([
        core_1.Output(),
        __metadata("design:type", core_1.EventEmitter)
    ], DropboxDownloadComponent.prototype, "downloadEvent", void 0);
    DropboxDownloadComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'dropbox-download',
            templateUrl: './dropbox-download.component.html',
            styleUrls: ['./dropbox-download.component.css']
        }),
        __metadata("design:paramtypes", [dropbox_service_1.DropboxService])
    ], DropboxDownloadComponent);
    return DropboxDownloadComponent;
}());
exports.DropboxDownloadComponent = DropboxDownloadComponent;
//# sourceMappingURL=dropbox-download.component.js.map