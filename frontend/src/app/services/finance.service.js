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
 * Created by Hanicz on 1/17/2018.
 */
var core_1 = require("@angular/core");
var http_1 = require("@angular/http");
require("rxjs/add/operator/map");
var common_1 = require("@angular/common");
var FinanceService = /** @class */ (function () {
    function FinanceService(datePipe, http) {
        this.datePipe = datePipe;
        this.http = http;
        this.headers = new http_1.Headers({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        });
        this.userUrl = 'http://localhost:5000/finances';
    }
    FinanceService.prototype.get_finances_by_year = function (year) {
        var url = this.userUrl + "/year/" + year;
        return this.http.get(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FinanceService.prototype.get_finances_by_month = function (year, month) {
        var url = this.userUrl + "/month?year=" + year + "&month=" + month;
        return this.http.get(url, {
            withCredentials: true,
        })
            .map(function (res) { return res.json(); });
    };
    FinanceService.prototype.get_finances_by_month_aggregated = function (year, month) {
        var url = this.userUrl + "/month/aggregated?year=" + year + "&month=" + month;
        return this.http.get(url, {
            withCredentials: true,
        })
            .map(function (res) { return res.json(); });
    };
    FinanceService.prototype.get_finances_by_year_aggregated = function (year) {
        var url = this.userUrl + "/year/aggregated/" + year;
        return this.http.get(url, {
            withCredentials: true,
        })
            .map(function (res) { return res.json(); });
    };
    FinanceService.prototype.update_finance = function (finance) {
        var url = this.userUrl + "/finance";
        return this.http.post(url, JSON.stringify(finance), {
            headers: this.headers,
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FinanceService.prototype.delete_finance = function (id) {
        var url = this.userUrl + "/finance/" + id;
        return this.http.delete(url, {
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FinanceService.prototype.new_finance = function (finance) {
        var data = {
            'amount': finance.amount,
            'comment': finance.comment,
            'finance_date': this.datePipe.transform(finance.finance_date, 'yyyy-MM-dd'),
            'finance_type_id': finance.finance_type_id
        };
        var url = this.userUrl + "/finance";
        return this.http.put(url, JSON.stringify(data), {
            headers: this.headers,
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FinanceService.prototype.get_finance_types = function () {
        var url = this.userUrl + "/types";
        return this.http.get(url, {
            withCredentials: true,
        })
            .map(function (res) { return res.json(); });
    };
    FinanceService.prototype.new_finance_type = function (name) {
        var url = this.userUrl + "/type?name=" + name;
        return this.http.put(url, null, {
            headers: this.headers,
            withCredentials: true
        })
            .map(function (res) { return res.json(); });
    };
    FinanceService = __decorate([
        core_1.Injectable(),
        __metadata("design:paramtypes", [common_1.DatePipe, http_1.Http])
    ], FinanceService);
    return FinanceService;
}());
exports.FinanceService = FinanceService;
//# sourceMappingURL=finance.service.js.map