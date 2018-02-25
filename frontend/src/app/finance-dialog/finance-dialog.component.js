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
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
Object.defineProperty(exports, "__esModule", { value: true });
var core_1 = require("@angular/core");
var material_1 = require("@angular/material");
var finance_service_1 = require("../services/finance.service");
var finance_1 = require("../entities/finance");
var FinanceDialog = /** @class */ (function () {
    function FinanceDialog(financeService, dialogRef, data) {
        this.financeService = financeService;
        this.dialogRef = dialogRef;
        this.data = data;
        this.finance = new finance_1.Finance();
        this.finance.finance_date = new Date();
        this.financeTypes = data.financeTypes;
    }
    FinanceDialog.prototype.createRecord = function () {
        this.finance.finance_type_id = this.selectedType.id;
        this.financeService.new_finance(this.finance).subscribe(function (json) {
        }, function (error) { return console.error('Error: ' + error); });
        this.dialogRef.close();
    };
    FinanceDialog.prototype.createType = function () {
        this.financeService.new_finance_type(this.newFinanceTypeName).subscribe(function (json) {
        }, function (error) { return console.error('Error: ' + error); });
    };
    FinanceDialog = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'finance-dialog',
            templateUrl: './finance-dialog.component.html',
            styleUrls: ['./finance-dialog.component.css']
        }),
        __param(2, core_1.Inject(material_1.MAT_DIALOG_DATA)),
        __metadata("design:paramtypes", [finance_service_1.FinanceService,
            material_1.MatDialogRef, Object])
    ], FinanceDialog);
    return FinanceDialog;
}());
exports.FinanceDialog = FinanceDialog;
//# sourceMappingURL=finance-dialog.component.js.map