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
require("rxjs/add/operator/map");
var NoteService = /** @class */ (function () {
    function NoteService(http) {
        this.http = http;
        this.headers = new http_1.Headers({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        });
        this.userUrl = 'http://localhost:5000/notes';
    }
    NoteService.prototype.get_notes = function () {
        var url = "" + this.userUrl;
        return this.http.get(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    NoteService.prototype.get_shared_notes = function () {
        var url = this.userUrl + "/shared";
        return this.http.get(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    NoteService.prototype.update_note = function (note) {
        var url = this.userUrl + "/update";
        return this.http.post(url, JSON.stringify(note), {
            headers: this.headers,
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    NoteService.prototype.delete_note = function (id) {
        var url = this.userUrl + "/" + id;
        return this.http.delete(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    NoteService.prototype.new_note = function (note) {
        var url = this.userUrl + "/note";
        return this.http.put(url, JSON.stringify(note), {
            headers: this.headers,
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    NoteService = __decorate([
        core_1.Injectable(),
        __metadata("design:paramtypes", [http_1.Http])
    ], NoteService);
    return NoteService;
}());
exports.NoteService = NoteService;
//# sourceMappingURL=note.service.js.map