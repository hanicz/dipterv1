/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { map } from "rxjs/operators";

@Injectable()
export class LogService {

  private headers = new Headers({
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  });

  //private userUrl = 'http://localhost:5000/resources/logs';
  private userUrl = '/resources/logs';

  constructor(private http: Http) { }

  get_logs() {
    const url = `${this.userUrl}`;
    return this.http.get(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  get_file_logs(file_id: Number) {
    const url = `${this.userUrl}/file/${file_id}`;
    return this.http.get(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  get_folder_logs(folder_id: Number) {
    const url = `${this.userUrl}/folder/${folder_id}`;
    return this.http.get(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

}
