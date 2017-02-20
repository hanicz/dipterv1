/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable }    from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { CustomResponse } from '../utils/customResponse'

import 'rxjs/add/operator/map';


@Injectable()
export class UserService {

  private headers = new Headers({'Content-Type': 'application/json'});
  private userUrl = 'http://localhost:5000/users';

  constructor(private http: Http) { }

  login_user(username: string, password: string) {

    let params: URLSearchParams = new URLSearchParams();
    params.set('username', username);
    params.set('password', password);

    const url = `${this.userUrl}/login`;
    return this.http.get(url,{
        search: params
      })
      .map((res: Response) => res.json());
  }

  regist_user(username: string, password: string, email: string) {
    let data = {
      username : username,
      password : password,
      email : email
    };

    const url = `${this.userUrl}/register`;
    return this.http.post(url,JSON.stringify(data),{headers:this.headers})
      .map((res: Response) => res.json());
  }
}
