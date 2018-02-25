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
var file_1 = require("../entities/file");
var file_service_1 = require("../services/file.service");
var role_service_1 = require("../services/role.service");
var share_service_1 = require("../services/share.service");
var ShareComponent = /** @class */ (function () {
    function ShareComponent(fileService, roleService, shareService) {
        this.fileService = fileService;
        this.roleService = roleService;
        this.shareService = shareService;
        this.closeEvent = new core_1.EventEmitter();
        this.changeEvent = new core_1.EventEmitter();
    }
    ShareComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.roleService.get_roles().subscribe(function (json) {
            console.log(json);
            _this.roles = json;
        }, function (error) { return console.error('Error: ' + error); });
    };
    ShareComponent.prototype.ngOnChanges = function (changes) {
        var _this = this;
        for (var propName in changes) {
            if (propName == "file" && this.file != undefined) {
                this.shareService.get_shares(this.file.id).subscribe(function (json) {
                    console.log(json);
                    _this.shares = json;
                }, function (error) { return console.error('Error: ' + error); });
            }
        }
    };
    ShareComponent.prototype.share = function () {
        var _this = this;
        this.shareService.shareFile(this.file.id, this.selectedRole.id, this.to_user).subscribe(function (json) {
            console.log(json);
            _this.to_user = "";
            _this.selectedRole = null;
            _this.changeEvent.emit("File successfully shared");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("File sharing failed");
        });
    };
    ShareComponent.prototype.isValid = function () {
        return this.file.publicLink != null;
    };
    ShareComponent.prototype.makePublic = function () {
        var _this = this;
        this.shareService.makePublic(this.file.id).subscribe(function (json) {
            console.log(json);
            _this.changeEvent.emit("File made public successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("File public failed");
        });
    };
    ShareComponent.prototype.revokePublic = function () {
        var _this = this;
        this.shareService.revokePublic(this.file.id).subscribe(function (json) {
            console.log(json);
            _this.changeEvent.emit("File made private successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.changeEvent.emit("File private failed");
        });
    };
    ShareComponent.prototype.delete_share = function (share) {
        var _this = this;
        this.shareService.revoke_share(share.id).subscribe(function (json) {
            console.log(json);
            _this.shares.splice(_this.shares.indexOf(share), 1);
        }, function (error) { return console.error('Error: ' + error); });
    };
    ShareComponent.prototype.close = function () {
        this.closeEvent.emit();
    };
    __decorate([
        core_1.Input(),
        __metadata("design:type", file_1.MyFile)
    ], ShareComponent.prototype, "file", void 0);
    __decorate([
        core_1.Output(),
        __metadata("design:type", Object)
    ], ShareComponent.prototype, "closeEvent", void 0);
    __decorate([
        core_1.Output(),
        __metadata("design:type", core_1.EventEmitter)
    ], ShareComponent.prototype, "changeEvent", void 0);
    ShareComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'share',
            templateUrl: './share.component.html',
            styleUrls: ['./share.component.css']
        }),
        __metadata("design:paramtypes", [file_service_1.FileService,
            role_service_1.RoleService,
            share_service_1.ShareService])
    ], ShareComponent);
    return ShareComponent;
}());
exports.ShareComponent = ShareComponent;
//# sourceMappingURL=share.component.js.map