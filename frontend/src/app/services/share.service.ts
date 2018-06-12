/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { map } from "rxjs/operators";



@Injectable()
export class ShareService {

    private headers = new Headers({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    });

    //private userUrl = 'http://localhost:5000/resources/shares';
    private userUrl = '/resources/shares';

    constructor(private http: Http) { }


    makePublic(file_id: Number) {

        const url = `${this.userUrl}/public/${file_id}`;
        return this.http.put(url, null, {
            withCredentials: true
        }).pipe(
            map((res: Response) => res.json()));
    }

    revokePublic(file_id: Number) {

        const url = `${this.userUrl}/private/${file_id}`;
        return this.http.put(url, null, {
            withCredentials: true
        }).pipe(
            map((res: Response) => res.json()));
    }

    shareFile(file_id: Number, role_id: Number, to: String) {

        var data = {
            'file_id': file_id,
            'role_id': role_id,
            'to_user': to
        };

        const url = `${this.userUrl}/share`;
        return this.http.post(url, JSON.stringify(data), {
            headers: this.headers,
            withCredentials: true
        }).pipe(map((res: Response) => res.json()));
    }

    get_shares(file_id: Number) {
        const url = `${this.userUrl}/${file_id}`;
        return this.http.get(url, {
            withCredentials: true
        }).pipe(
            map((res: Response) => res.json()));
    }

    revoke_share(share_id: Number) {
        const url = `${this.userUrl}/revoke/${share_id}`;
        return this.http.delete(url, {
            withCredentials: true
        }).pipe(
            map((res: Response) => res.json()));
    }
}
