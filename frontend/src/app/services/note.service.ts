/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { MyFile } from '../entities/file';
import { map } from "rxjs/operators";



@Injectable()
export class NoteService {

  private headers = new Headers({
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  });

  //private userUrl = 'http://localhost:5000/resources/notes';
  private userUrl = '/resources/notes';

  constructor(private http: Http) { }

  get_notes() {
    const url = `${this.userUrl}`;
    return this.http.get(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  get_shared_notes() {
    const url = `${this.userUrl}/shared`;
    return this.http.get(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  update_note(note: MyFile){
    const url = `${this.userUrl}/update`;
    return this.http.post(url,JSON.stringify(note), {
      headers: this.headers,
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  delete_note(id: Number){
    const url = `${this.userUrl}/${id}`;
    return this.http.delete(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  new_note(note: MyFile){
    const url = `${this.userUrl}/note`;
    return this.http.put(url,JSON.stringify(note), {
      headers: this.headers,
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }
}
