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
var core_1 = require("@angular/core");
var chart_js_1 = require("chart.js");
var finance_service_1 = require("../services/finance.service");
var material_1 = require("@angular/material");
var material_2 = require("@angular/material");
var finance_dialog_component_1 = require("../finance-dialog/finance-dialog.component");
var common_1 = require("@angular/common");
var FinanceComponent = /** @class */ (function () {
    function FinanceComponent(financeService, dialog, datePipe) {
        this.financeService = financeService;
        this.dialog = dialog;
        this.datePipe = datePipe;
        this.chartHidden = true;
        this.displayedColumns = ['type', 'amount', 'comment', 'date'];
        this.dataSource = new material_1.MatTableDataSource(this.chartFinances);
    }
    FinanceComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.labels = [];
        this.amounts = [];
        this.colors = [];
        this.financeService.get_finance_types().subscribe(function (json) {
            console.log(json);
            _this.financeTypes = json;
        }, function (error) { return console.error('Error: ' + error); });
    };
    FinanceComponent.prototype.fill_chart = function () {
        var _this = this;
        if (this.aggr_year != null) {
            if (this.aggr_month != null) {
                this.financeService.get_finances_by_month_aggregated(this.aggr_year, this.aggr_month).subscribe(function (json) {
                    console.log(json);
                    _this.labels = [];
                    _this.amounts = [];
                    _this.colors = [];
                    _this.chartFinances = json;
                    _this.build_chart();
                }, function (error) { return console.error('Error: ' + error); });
            }
            else {
                this.financeService.get_finances_by_year_aggregated(this.aggr_year).subscribe(function (json) {
                    console.log(json);
                    _this.labels = [];
                    _this.amounts = [];
                    _this.colors = [];
                    _this.chartFinances = json;
                    _this.build_chart();
                }, function (error) { return console.error('Error: ' + error); });
            }
        }
    };
    FinanceComponent.prototype.get_formatted_date = function (date) {
        return this.datePipe.transform(date, 'yyyy-MM-dd');
    };
    FinanceComponent.prototype.get_finance_type_name = function (id) {
        var retVal;
        this.financeTypes.forEach(function (f) {
            if (f.id == id) {
                retVal = f.name;
            }
        });
        return retVal;
    };
    FinanceComponent.prototype.build_chart = function () {
        var _this = this;
        this.dataSource = new material_1.MatTableDataSource(this.chartFinances);
        this.chartFinances.forEach(function (f) {
            _this.labels.push(f.type);
            _this.amounts.push(f.sum);
            _this.colors.push(_this.getRandomColor());
        });
        this.chart = new chart_js_1.Chart('canvas', {
            type: 'pie',
            data: {
                labels: this.labels,
                datasets: [
                    {
                        data: this.amounts,
                        backgroundColor: this.colors
                    }
                ]
            },
            options: {
                title: {
                    display: true,
                    text: 'Finance records'
                }
            }
        });
    };
    FinanceComponent.prototype.getRandomColor = function () {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    };
    FinanceComponent.prototype.openDialog = function () {
        var dialogRef = this.dialog.open(finance_dialog_component_1.FinanceDialog, {
            data: { financeTypes: this.financeTypes }
        });
        dialogRef.afterClosed().subscribe(function (result) {
        });
    };
    FinanceComponent.prototype.applyFilter = function (filterValue) {
        filterValue = filterValue.trim();
        filterValue = filterValue.toLowerCase();
        this.dataSource.filter = filterValue;
    };
    FinanceComponent.prototype.fillTable = function () {
        var _this = this;
        if (this.year != null) {
            if (this.month == null) {
                this.financeService.get_finances_by_year(this.year).subscribe(function (json) {
                    console.log(json);
                    _this.chartFinances = json;
                    _this.dataSource = new material_1.MatTableDataSource(_this.chartFinances);
                }, function (error) { return console.error('Error: ' + error); });
            }
            else {
                this.financeService.get_finances_by_month(this.year, this.month).subscribe(function (json) {
                    console.log(json);
                    _this.chartFinances = json;
                    _this.dataSource = new material_1.MatTableDataSource(_this.chartFinances);
                }, function (error) { return console.error('Error: ' + error); });
            }
        }
    };
    FinanceComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'finance',
            templateUrl: './finance.component.html',
            styleUrls: ['./finance.component.css']
        }),
        __metadata("design:paramtypes", [finance_service_1.FinanceService,
            material_2.MatDialog,
            common_1.DatePipe])
    ], FinanceComponent);
    return FinanceComponent;
}());
exports.FinanceComponent = FinanceComponent;
//# sourceMappingURL=finance.component.js.map