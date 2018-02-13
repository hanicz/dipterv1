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
var CreateFolderComponent = /** @class */ (function () {
    function CreateFolderComponent(fileService) {
        this.fileService = fileService;
        this.closeEvent = new core_1.EventEmitter();
        this.newFolder = new folder_1.Folder();
    }
    CreateFolderComponent.prototype.create = function () {
        var _this = this;
        this.newFolder.parent = this.folder;
        this.fileService.create_folder(this.newFolder).subscribe(function (json) {
            console.log(json);
            _this.newFolder = new folder_1.Folder();
            _this.closeEvent.emit();
        }, function (error) { return console.error('Error: ' + error); });
    };
    CreateFolderComponent.prototype.close = function () {
        this.closeEvent.emit();
    };
    __decorate([
        core_1.Input(),
        __metadata("design:type", Number)
    ], CreateFolderComponent.prototype, "folder", void 0);
    __decorate([
        core_1.Output(),
        __metadata("design:type", Object)
    ], CreateFolderComponent.prototype, "closeEvent", void 0);
    CreateFolderComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'create-folder',
            templateUrl: './create-folder.component.html',
            styleUrls: ['./create-folder.component.css']
        }),
        __metadata("design:paramtypes", [file_service_1.FileService])
    ], CreateFolderComponent);
    return CreateFolderComponent;
}());
exports.CreateFolderComponent = CreateFolderComponent;
//# sourceMappingURL=create-folder.component.js.map