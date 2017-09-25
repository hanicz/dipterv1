/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { CustomResponse } from '../utils/customResponse'

import 'rxjs/add/operator/map';



@Injectable()
export class ShareService {

    private headers = new Headers({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    });

    private userUrl = 'http://localhost:5000/shares';

    constructor(private http: Http) { }


    makePublic(file_id: Number) {

        const url = `${this.userUrl}/makePublic/${file_id}`;
        return this.http.put(url, null, {
            withCredentials: true
        })
            .map((res: Response) => res.json());
    }

    revokePublic(file_id: Number) {

        const url = `${this.userUrl}/revokePublic/${file_id}`;
        return this.http.put(url, null, {
            withCredentials: true
        })
            .map((res: Response) => res.json());
    }

    shareFile(file_id: Number, role_id: Number, to: String){
        
        var data = {
            'file_id': file_id,
            'role_id': role_id,
            'to_user': to
        };

        const url = `${this.userUrl}/shareFile`;
        return this.http.post(url, JSON.stringify(data), {
            headers: this.headers,
            withCredentials: true
        }).map((res: Response) => res.json());
    }
}
