/**
 * Created by Hanicz on 1/17/2018.
 */
import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { Finance } from '../entities/Finance';
import { map } from "rxjs/operators";
import { DatePipe } from '@angular/common';

@Injectable()
export class FinanceService {

    private headers = new Headers({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    });

    private userUrl = 'http://localhost:5000/resources/finances';
    //private userUrl = '/resources/finances';

    constructor(private datePipe: DatePipe, private http: Http) { }

    get_finances_by_year(year: Number) {
        const url = `${this.userUrl}/year/${year}`;
        return this.http.get(url, {
            withCredentials: true
        }).pipe(
            map((res: Response) => res.json()));
    }

    get_finances_by_month(year: Number, month: Number) {
        const url = `${this.userUrl}/month?year=${year}&month=${month}`;
        return this.http.get(url, {
            withCredentials: true,
        }).pipe(
            map((res: Response) => res.json()));
    }

    get_finances_by_month_aggregated(year: Number, month: Number) {
        const url = `${this.userUrl}/month/aggregated?year=${year}&month=${month}`;
        return this.http.get(url, {
            withCredentials: true,
        }).pipe(
            map((res: Response) => res.json()));
    }

    get_finances_by_year_aggregated(year: Number) {
        const url = `${this.userUrl}/year/aggregated/${year}`;
        return this.http.get(url, {
            withCredentials: true,
        }).pipe(
            map((res: Response) => res.json()));
    }

    update_finance(finance: Finance) {

        var data = {
            'finance_id': finance.id,
            'amount': finance.amount,
            'comment': finance.comment,
            'finance_date': this.datePipe.transform(finance.finance_date, 'yyyy-MM-dd'),
            'finance_type_id': finance.finance_type_id
        }

        const url = `${this.userUrl}/finance`;
        return this.http.post(url, JSON.stringify(data), {
            headers: this.headers,
            withCredentials: true
        }).pipe(
            map((res: Response) => res.json()));
    }

    delete_finance(id: Number) {
        const url = `${this.userUrl}/finance/${id}`;
        return this.http.delete(url, {
            withCredentials: true
        }).pipe(
            map((res: Response) => res.json()));
    }

    new_finance(finance: Finance) {

        var data = {
            'amount': finance.amount,
            'comment': finance.comment,
            'finance_date': this.datePipe.transform(finance.finance_date, 'yyyy-MM-dd'),
            'finance_type_id': finance.finance_type_id
        }

        const url = `${this.userUrl}/finance`;
        return this.http.put(url, JSON.stringify(data), {
            headers: this.headers,
            withCredentials: true
        }).pipe(
            map((res: Response) => res.json()));
    }

    get_finance_types() {
        const url = `${this.userUrl}/types`;
        return this.http.get(url, {
            withCredentials: true,
        }).pipe(
            map((res: Response) => res.json()));
    }

    new_finance_type(name: String) {

        const url = `${this.userUrl}/type?name=${name}`;
        return this.http.put(url, null, {
            headers: this.headers,
            withCredentials: true
        }).pipe(
            map((res: Response) => res.json()));
    }
}
