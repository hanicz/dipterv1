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

  get_notes() {
    const url = `${this.userUrl}/userNotes`;
    return this.http.get(url, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  update_note(note: MyFile){
    const url = `${this.userUrl}/updateNote`;
    return this.http.post(url,JSON.stringify(note), {
      headers: this.headers,
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  delete_note(id: Number){
    const url = `${this.userUrl}/deleteNote/${id}`;
    return this.http.delete(url, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  new_note(note: MyFile){
    const url = `${this.userUrl}/note`;
    return this.http.put(url,JSON.stringify(note), {
      headers: this.headers,
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }
}
