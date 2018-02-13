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
var http_2 = require("@angular/http");
require("rxjs/add/operator/map");
var FileService = /** @class */ (function () {
    function FileService(http) {
        this.http = http;
        this.formDataHeaders = new http_1.Headers({
            'Content-Type': 'multipart/form-data',
            'Accept': 'application/json'
        });
        this.jsonHeaders = new http_1.Headers({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        });
        this.userUrl = 'http://localhost:5000/files';
    }
    FileService.prototype.upload_file = function (file, folder_id) {
        var headers = new http_1.Headers();
        var formData = new FormData();
        formData.append('file', file[0], file[0].name);
        console.log(file[0].name);
        // for (let i = 0; i < files.length; i++) {
        //     formData.append(`files[]`, files[i], files[i].name);
        // }
        var url = this.userUrl + "/file/" + folder_id;
        return this.http.post(url, formData, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FileService.prototype.download = function (file_id) {
        var url = this.userUrl + "/download/" + file_id;
        var options = new http_2.RequestOptions({ responseType: http_2.ResponseContentType.Blob,
            withCredentials: true });
        return this.http.get(url, options).map(function (res) { return res.blob(); });
    };
    FileService.prototype.get_files = function (folder_id) {
        var url = this.userUrl + "/file/" + folder_id;
        return this.http.get(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FileService.prototype.get_deleted_files = function () {
        var url = this.userUrl + "/file/deleted";
        return this.http.get(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FileService.prototype.get_folders = function (folder_id) {
        var url = this.userUrl + "/folder/" + folder_id;
        return this.http.get(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FileService.prototype.get_deleted_folders = function () {
        var url = this.userUrl + "/folder/deleted";
        return this.http.get(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FileService.prototype.rename_file = function (file) {
        var url = this.userUrl + "/file/rename";
        return this.http.put(url, JSON.stringify(file), {
            headers: this.jsonHeaders,
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FileService.prototype.rename_folder = function (folder) {
        var url = this.userUrl + "/folder/rename";
        return this.http.put(url, JSON.stringify(folder), {
            headers: this.jsonHeaders,
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FileService.prototype.remove_file = function (id) {
        var url = this.userUrl + "/file/" + id;
        return this.http.delete(url, {
            withCredentials: true
        }).map(function (res) { return res.json(); });
    };
    FileService.prototype.remove_folder = function (id) {
        var url = this.userUrl + "/folder/" + id;
        return this.http.delete(url, {
            withCredentials: true
        }).map(function (res) { return res.json(); });
    };
    FileService.prototype.get_folder_list = function () {
        var url = this.userUrl + "/folder/list";
        return this.http.get(url, {
            withCredentials: true
        }).map(function (res) { return res.json(); });
    };
    FileService.prototype.move_file = function (folder_id, file_id) {
        var data = {
            'file_id': file_id,
            'new_folder_id': folder_id
        };
        var url = this.userUrl + "/file/move";
        return this.http.put(url, JSON.stringify(data), {
            headers: this.jsonHeaders,
            withCredentials: true
        }).map(function (res) { return res.json(); });
    };
    FileService.prototype.move_folder = function (folder_id, parent_id) {
        var data = {
            'folder_id': folder_id,
            'parent_id': parent_id
        };
        var url = this.userUrl + "/folder/move";
        return this.http.put(url, JSON.stringify(data), {
            headers: this.jsonHeaders,
            withCredentials: true
        }).map(function (res) { return res.json(); });
    };
    FileService.prototype.restore_file = function (file_id) {
        var url = this.userUrl + "/file/restore/" + file_id;
        return this.http.put(url, null, {
            withCredentials: true
        }).map(function (res) { return res.json(); });
    };
    FileService.prototype.restore_folder = function (folder_id) {
        var url = this.userUrl + "/folder/restore/" + folder_id;
        return this.http.put(url, null, {
            withCredentials: true
        }).map(function (res) { return res.json(); });
    };
    FileService.prototype.create_folder = function (folder) {
        var data = {
            'folderName': folder.folderName,
            'parent': String(folder.parent)
        };
        var url = this.userUrl + "/createFolder";
        return this.http.post(url, JSON.stringify(data), {
            headers: this.jsonHeaders,
            withCredentials: true
        }).map(function (res) { return res.json(); });
    };
    FileService.prototype.get_shared_with_me_files = function () {
        var url = this.userUrl + "/shared";
        return this.http.get(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FileService.prototype.search_files = function (file_name) {
        var url = this.userUrl + "/search/" + file_name;
        return this.http.get(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FileService = __decorate([
        core_1.Injectable(),
        __metadata("design:paramtypes", [http_1.Http])
    ], FileService);
    return FileService;
}());
exports.FileService = FileService;
//# sourceMappingURL=file.service.js.map