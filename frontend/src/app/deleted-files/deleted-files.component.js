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
var folder_1 = require("../entities/folder");
var DeletedFilesComponent = /** @class */ (function () {
    function DeletedFilesComponent(fileService) {
        this.fileService = fileService;
        this.folderHidden = true;
        this.fileHidden = true;
        this.responseHidden = true;
    }
    DeletedFilesComponent.prototype.ngOnInit = function () {
        this.selectedFolder = new folder_1.Folder();
        this.get_deleted_folders();
        this.get_deleted_files();
    };
    DeletedFilesComponent.prototype.get_deleted_files = function () {
        var _this = this;
        this.fileService.get_deleted_files().subscribe(function (json) {
            console.log(json);
            _this.files = json;
        }, function (error) { return console.error('Error: ' + error); });
    };
    DeletedFilesComponent.prototype.get_deleted_folders = function () {
        var _this = this;
        this.fileService.get_deleted_folders().subscribe(function (json) {
            console.log(json);
            _this.folders = json;
        }, function (error) { return console.error('Error: ' + error); });
    };
    DeletedFilesComponent.prototype.onSelectFile = function (file) {
        this.selectedFile = file;
        this.fileHidden = false;
        this.folderHidden = true;
    };
    DeletedFilesComponent.prototype.onSelectFolder = function (folder) {
        this.selectedFolder = folder;
        this.fileHidden = true;
        this.folderHidden = false;
    };
    DeletedFilesComponent.prototype.file_restored = function () {
        this.selectedFile = null;
        this.get_deleted_folders();
        this.get_deleted_files();
    };
    DeletedFilesComponent.prototype.showResponse = function (event) {
        var _this = this;
        this.requestResponse = event;
        this.responseHidden = false;
        setTimeout(function () { return _this.responseHidden = true; }, 2000);
    };
    DeletedFilesComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'deleted-files',
            templateUrl: './deleted-files.component.html',
            styleUrls: ['./deleted-files.component.css']
        }),
        __metadata("design:paramtypes", [file_service_1.FileService])
    ], DeletedFilesComponent);
    return DeletedFilesComponent;
}());
exports.DeletedFilesComponent = DeletedFilesComponent;
//# sourceMappingURL=deleted-files.component.js.map