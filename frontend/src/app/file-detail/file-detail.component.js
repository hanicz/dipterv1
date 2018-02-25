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
var http_1 = require("@angular/http");
var file_1 = require("../entities/file");
var file_service_1 = require("../services/file.service");
var log_service_1 = require("../services/log.service");
var dropbox_service_1 = require("../services/dropbox.service");
require("rxjs/add/operator/toPromise");
var FileDetailComponent = /** @class */ (function () {
    function FileDetailComponent(fileService, logService, dropboxService, http) {
        this.fileService = fileService;
        this.logService = logService;
        this.dropboxService = dropboxService;
        this.http = http;
        this.shareEvent = new core_1.EventEmitter();
        this.changeEvent = new core_1.EventEmitter();
    }
    FileDetailComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.fileService.get_folder_list().subscribe(function (json) {
            console.log(json);
            _this.folders = json;
        }, function (error) { return console.error('Error: ' + error); });
    };
    FileDetailComponent.prototype.ngOnChanges = function (changes) {
        var _this = this;
        for (var propName in changes) {
            if (propName == "file" && this.file != undefined) {
                this.logService.get_file_logs(this.file.id).subscribe(function (json) {
                    console.log(json);
                    _this.logs = json;
                }, function (error) { return console.error('Error: ' + error); });
            }
        }
    };
    FileDetailComponent.prototype.rename = function () {
        var _this = this;
        this.fileService.rename_file(this.file).subscribe(function (json) {
            console.log(json);
            _this.changeEvent.emit("File renamed successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("File rename failed");
        });
    };
    FileDetailComponent.prototype.delete = function () {
        var _this = this;
        this.fileService.remove_file(this.file.id).subscribe(function (json) {
            console.log(json);
            _this.file = null;
            _this.changeEvent.emit("File deleted successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("File delete failed");
        });
    };
    FileDetailComponent.prototype.isValid = function () {
        return this.file.deleted != null;
    };
    FileDetailComponent.prototype.share = function () {
        this.shareEvent.emit();
    };
    FileDetailComponent.prototype.move = function () {
        var _this = this;
        this.fileService.move_file(this.moveFolder.id, this.file.id).subscribe(function (json) {
            console.log(json);
            _this.changeEvent.emit("File moved successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("File move failed");
        });
    };
    FileDetailComponent.prototype.restore = function () {
        var _this = this;
        this.fileService.restore_file(this.file.id).subscribe(function (json) {
            console.log(json);
            _this.changeEvent.emit("File restored successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("File restore failed");
        });
    };
    FileDetailComponent.prototype.dropbox = function () {
        var _this = this;
        this.dropboxService.upload_to_dropbox(this.file.id).subscribe(function (json) {
            console.log(json);
            _this.changeEvent.emit("File uploaded to dropbox successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("File upload to dropbox failed");
        });
    };
    FileDetailComponent.prototype.download = function () {
        /*var userUrl = 'http://192.168.1.2:5000/files';
        
        const url = `${userUrl}/download/${this.file.id}`;
        
        var config = { responseType: ResponseContentType.Blob, withCredentials: true };
            
        return this.http.get(url, config).toPromise()
                .then(function (response) {
                    var data = response.blob();
                    saveAs(data, name);
                })
                .catch(function (err) {
                    alert("It has happened an error. Downloading has been stopped") ;
                    throw err;
                });*/
        var newWindow = window.open('http://localhost:5000/files/download/' + this.file.id);
        /*this.fileService.download(this.file.id).subscribe(blob => {
          this.changeEvent.emit("File download started successfully");
          saveAs(blob, this.file.fileName.toString());
        });*/
    };
    __decorate([
        core_1.Input(),
        __metadata("design:type", file_1.MyFile)
    ], FileDetailComponent.prototype, "file", void 0);
    __decorate([
        core_1.Output(),
        __metadata("design:type", Object)
    ], FileDetailComponent.prototype, "shareEvent", void 0);
    __decorate([
        core_1.Output(),
        __metadata("design:type", core_1.EventEmitter)
    ], FileDetailComponent.prototype, "changeEvent", void 0);
    FileDetailComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'file-detail',
            templateUrl: './file-detail.component.html',
            styleUrls: ['./file-detail.component.css']
        }),
        __metadata("design:paramtypes", [file_service_1.FileService,
            log_service_1.LogService,
            dropbox_service_1.DropboxService,
            http_1.Http])
    ], FileDetailComponent);
    return FileDetailComponent;
}());
exports.FileDetailComponent = FileDetailComponent;
//# sourceMappingURL=file-detail.component.js.map