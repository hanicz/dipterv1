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
var file_service_1 = require("../services/file.service");
var log_service_1 = require("../services/log.service");
var FolderDetailComponent = /** @class */ (function () {
    function FolderDetailComponent(fileService, logService) {
        this.fileService = fileService;
        this.logService = logService;
        this.changeEvent = new core_1.EventEmitter();
    }
    FolderDetailComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.fileService.get_folder_list().subscribe(function (json) {
            console.log(json);
            _this.folders = json;
        }, function (error) { return console.error('Error: ' + error); });
    };
    FolderDetailComponent.prototype.ngOnChanges = function (changes) {
        var _this = this;
        for (var propName in changes) {
            if (propName == "folder" && this.folder != undefined) {
                this.logService.get_folder_logs(this.folder.id).subscribe(function (json) {
                    console.log(json);
                    _this.logs = json;
                }, function (error) { return console.error('Error: ' + error); });
            }
        }
    };
    FolderDetailComponent.prototype.isValid = function () {
        return this.folder.deleted != null;
    };
    FolderDetailComponent.prototype.rename = function () {
        var _this = this;
        this.fileService.rename_folder(this.folder).subscribe(function (json) {
            console.log(json);
            _this.changeEvent.emit("Folder renamed successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("Folder rename failed");
        });
    };
    FolderDetailComponent.prototype.delete = function () {
        var _this = this;
        this.fileService.remove_folder(this.folder.id).subscribe(function (json) {
            console.log(json);
            _this.folder = null;
            _this.changeEvent.emit("Folder deleted successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("Folder delete failed");
        });
    };
    FolderDetailComponent.prototype.move = function () {
        var _this = this;
        this.fileService.move_folder(this.folder.id, this.moveFolder.id).subscribe(function (json) {
            console.log(json);
            _this.changeEvent.emit("Folder moved successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("Folder move failed");
        });
    };
    FolderDetailComponent.prototype.restore = function () {
        var _this = this;
        this.fileService.restore_folder(this.folder.id).subscribe(function (json) {
            console.log(json);
            _this.changeEvent.emit("Folder restored successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("Folder restore failed");
        });
    };
    FolderDetailComponent.prototype.download = function () {
        var newWindow = window.open('http://localhost:5000/files/download/folder/' + this.folder.id);
        /*this.fileService.download(this.file.id).subscribe(blob => {
          this.changeEvent.emit("File download started successfully");
          saveAs(blob, this.file.fileName.toString());
        });*/
    };
    __decorate([
        core_1.Input(),
        __metadata("design:type", folder_1.Folder)
    ], FolderDetailComponent.prototype, "folder", void 0);
    __decorate([
        core_1.Output(),
        __metadata("design:type", core_1.EventEmitter)
    ], FolderDetailComponent.prototype, "changeEvent", void 0);
    FolderDetailComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'folder-detail',
            templateUrl: './folder-detail.component.html',
            styleUrls: ['./folder-detail.component.css']
        }),
        __metadata("design:paramtypes", [file_service_1.FileService,
            log_service_1.LogService])
    ], FolderDetailComponent);
    return FolderDetailComponent;
}());
exports.FolderDetailComponent = FolderDetailComponent;
//# sourceMappingURL=folder-detail.component.js.map