/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { map } from "rxjs/operators";



@Injectable()
export class DropboxService {

    private headers = new Headers({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    });

    //private userUrl = 'http://localhost:5000/resources/dropbox';
    private userUrl = '/resources/dropbox';

    constructor(private http: Http) { }

    get_url() {
        const url = `${this.userUrl}`;
        return this.http.get(url, {
            withCredentials: true
        }).pipe(map((res: Response) => res.json()));
    }

    finish_auth(token: String) {
        var data = {
            'token': token
        };
        const url = `${this.userUrl}`;
        return this.http.post(url, JSON.stringify(data), {
            headers: this.headers,
            withCredentials: true
        }).pipe(map((res: Response) => res.json()));
    }

    upload_to_dropbox(file_id: Number) {
        const url = `${this.userUrl}/upload/${file_id}`;
        return this.http.post(url, null, {
            withCredentials: true
        }).pipe(map((res: Response) => res.json()));
    }

    download_from_dropbox(path: String, filename: String, folder_id: Number) {
        var data = {
            'path': path,
            'file_name': filename,
            'folder_id': folder_id.toString()
        };

        const url = `${this.userUrl}/download`;
        return this.http.post(url, JSON.stringify(data), {
            headers: this.headers,
            withCredentials: true
        }).pipe(map((res: Response) => res.json()));
    }
}
