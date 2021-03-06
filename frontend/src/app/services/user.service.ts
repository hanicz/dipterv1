/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { map } from "rxjs/operators";
import { User } from '../utils/user'
import { ResetUser } from '../entities/reset-user'
import { ChangeUser } from '../entities/changeuser'


@Injectable()
export class UserService {

  private headers = new Headers({
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  });

  //private userUrl = 'http://localhost:5000/resources/users';
  private userUrl = '/resources/users';

  constructor(private http: Http) { }

  login_user(user: User) {
    const url = `${this.userUrl}/login`;
    return this.http.post(url, JSON.stringify(user), {
      headers: this.headers,
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  register_user(user: User) {

    const url = `${this.userUrl}/register`;
    return this.http.post(url, JSON.stringify(user), { headers: this.headers }).pipe(
      map((res: Response) => res.json()));
  }

  activate_user(token: String) {
    const url = `${this.userUrl}/activate/${token}`;
    return this.http.put(url, '', { headers: this.headers }).pipe(
      map((res: Response) => res.json()));
  }

  reset_user(user: ResetUser) {
    const url = `${this.userUrl}/reset`;
    return this.http.put(url, JSON.stringify(user), { headers: this.headers }).pipe(
      map((res: Response) => res.json()));
  }

  changedata(user: ChangeUser) {
    const url = `${this.userUrl}/change`;
    return this.http.put(url, JSON.stringify(user), {
      headers: this.headers,
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  logout() {
    const url = `${this.userUrl}/logout`;
    return this.http.put(url, null, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  delete() {
    const url = `${this.userUrl}/delete`;
    return this.http.delete(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }
}
