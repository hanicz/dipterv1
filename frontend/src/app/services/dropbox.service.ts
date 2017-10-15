/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { CustomResponse } from '../utils/customResponse'

import 'rxjs/add/operator/map';



@Injectable()
export class DropboxService {

    private headers = new Headers({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    });

    private userUrl = 'http://localhost:5000/dropbox';

    constructor(private http: Http) { }

    get_url() {
        const url = `${this.userUrl}`;
        return this.http.get(url, {
            withCredentials: true
        })
            .map((res: Response) => res.json());
    }

    finish_auth(token: String) {
        var data = {
            'token': token
        };
        const url = `${this.userUrl}`;
        return this.http.post(url, JSON.stringify(data), {
            headers: this.headers,
            withCredentials: true
        })
            .map((res: Response) => res.json());
    }

    upload_to_dropbox(file_id: Number){
        const url = `${this.userUrl}/upload/${file_id}`;
        return this.http.post(url, null, {
            withCredentials: true
        })
            .map((res: Response) => res.json());
    }
}
