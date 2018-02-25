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
var FilesComponent = /** @class */ (function () {
    function FilesComponent(fileService) {
        this.fileService = fileService;
        this.uploadHidden = true;
        this.uploadShare = true;
        this.createFolderHidden = true;
        this.prevent = false;
        this.folderHidden = true;
        this.fileHidden = true;
        this.responseHidden = true;
        this.dropboxHidden = true;
    }
    FilesComponent.prototype.ngOnInit = function () {
        this.selectedFolder = new folder_1.Folder();
        this.selectedFolder.id = 0;
        this.currentFolder = new folder_1.Folder();
        this.currentFolder.id = 0;
        this.get_folders(this.currentFolder);
        this.get_files(0);
    };
    FilesComponent.prototype.get_files = function (folder_id) {
        var _this = this;
        this.fileService.get_files(folder_id).subscribe(function (json) {
            console.log(json);
            _this.files = json;
        }, function (error) { return console.error('Error: ' + error); });
    };
    FilesComponent.prototype.get_folders = function (folder) {
        var _this = this;
        this.fileService.get_folders(folder.id).subscribe(function (json) {
            console.log(json);
            _this.folders = json;
        }, function (error) { return console.error('Error: ' + error); });
    };
    FilesComponent.prototype.onSelectFile = function (file) {
        this.selectedFile = file;
        this.fileHidden = false;
        this.folderHidden = true;
    };
    FilesComponent.prototype.onSelectFolder = function (folder) {
        if (folder.folderName != '...') {
            this.fileHidden = true;
            this.folderHidden = false;
            this.selectedFolder = folder;
        }
        else {
            this.folderHidden = true;
            this.fileHidden = true;
        }
    };
    FilesComponent.prototype.onDblSelectFolder = function (folder) {
        this.folderHidden = true;
        this.fileHidden = true;
        this.currentFolder = folder;
        this.get_files(folder.id);
        this.get_folders(folder);
    };
    FilesComponent.prototype.showUpload = function () {
        this.uploadHidden = false;
    };
    FilesComponent.prototype.showShare = function () {
        this.uploadShare = false;
    };
    FilesComponent.prototype.showFolder = function () {
        this.createFolderHidden = false;
    };
    FilesComponent.prototype.close_upload = function () {
        this.uploadHidden = true;
        this.createFolderHidden = true;
        this.get_files(this.currentFolder.id);
        this.get_folders(this.currentFolder);
    };
    FilesComponent.prototype.search_files = function (newValue) {
        var _this = this;
        this.folderHidden = true;
        this.fileHidden = true;
        this.search = newValue;
        if (newValue == "") {
            this.get_files(this.currentFolder.id);
            this.get_folders(this.currentFolder);
        }
        else {
            this.fileService.search_files(this.search).subscribe(function (json) {
                console.log(json);
                _this.files = json;
                _this.folders = null;
            }, function (error) { return console.error('Error: ' + error); });
        }
    };
    FilesComponent.prototype.showResponse = function (event) {
        var _this = this;
        this.requestResponse = event;
        this.responseHidden = false;
        setTimeout(function () { return _this.responseHidden = true; }, 2000);
    };
    FilesComponent.prototype.showDropbox = function (event) {
        this.dropboxHidden = false;
    };
    FilesComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'files',
            templateUrl: './files.component.html',
            styleUrls: ['./files.component.css']
        }),
        __metadata("design:paramtypes", [file_service_1.FileService])
    ], FilesComponent);
    return FilesComponent;
}());
exports.FilesComponent = FilesComponent;
//# sourceMappingURL=files.component.js.map