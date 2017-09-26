/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { CustomResponse } from '../utils/customResponse'
import { MyFile } from '../entities/file';

import 'rxjs/add/operator/map';



@Injectable()
export class NoteService {

  private headers = new Headers({
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  });

  private userUrl = 'http://localhost:5000/notes';

  constructor(private http: Http) { }

  get_files() {
    const url = `${this.userUrl}/userNotes`;
    return this.http.get(url, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }
}
