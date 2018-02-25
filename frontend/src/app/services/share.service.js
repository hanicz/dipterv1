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
var ShareService = /** @class */ (function () {
    function ShareService(http) {
        this.http = http;
        this.headers = new http_1.Headers({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        });
        this.userUrl = 'http://localhost:5000/shares';
    }
    ShareService.prototype.makePublic = function (file_id) {
        var url = this.userUrl + "/public/" + file_id;
        return this.http.put(url, null, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    ShareService.prototype.revokePublic = function (file_id) {
        var url = this.userUrl + "/private/" + file_id;
        return this.http.put(url, null, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    ShareService.prototype.shareFile = function (file_id, role_id, to) {
        var data = {
            'file_id': file_id,
            'role_id': role_id,
            'to_user': to
        };
        var url = this.userUrl + "/share";
        return this.http.post(url, JSON.stringify(data), {
            headers: this.headers,
            withCredentials: true
        }).map(function (res) { return res.json(); });
    };
    ShareService.prototype.get_shares = function (file_id) {
        var url = this.userUrl + "/" + file_id;
        return this.http.get(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    ShareService.prototype.revoke_share = function (share_id) {
        var url = this.userUrl + "/revoke/" + share_id;
        return this.http.delete(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    ShareService = __decorate([
        core_1.Injectable(),
        __metadata("design:paramtypes", [http_1.Http])
    ], ShareService);
    return ShareService;
}());
exports.ShareService = ShareService;
//# sourceMappingURL=share.service.js.map