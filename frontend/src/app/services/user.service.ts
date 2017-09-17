/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable }    from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { CustomResponse } from '../utils/customResponse'

import 'rxjs/add/operator/map';

import { User } from '../utils/user'
import { ResetUser } from '../entities/reset-user'
import { ChangeUser } from '../entities/changeuser'


@Injectable()
export class UserService {

  private headers = new Headers({'Content-Type': 'application/json',
                                  'Accept': 'application/json'});
  private userUrl = 'http://localhost:5000/users';

  constructor(private http: Http) { }

  login_user(user: User) {

   /* let params: URLSearchParams = new URLSearchParams();
    params.set('username', username);
    params.set('password', password);*/

    const url = `${this.userUrl}/login`;
    return this.http.post(url,JSON.stringify(user),{
        headers:this.headers,
        withCredentials: true
      })
      .map((res: Response) => res.json());
  }

  register_user(user: User) {

    const url = `${this.userUrl}/register`;
    return this.http.post(url,JSON.stringify(user),{headers:this.headers})
      .map((res: Response) => res.json());
  }

  activate_user(token: String){
    const url = `${this.userUrl}/activate/${token}`;
    return this.http.put(url,'',{headers:this.headers})
      .map((res: Response) => res.json());
  }

  reset_user(user: ResetUser){
    const url = `${this.userUrl}/reset`;
    return this.http.put(url,JSON.stringify(user),{headers:this.headers})
      .map((res: Response) => res.json());
  }

  logout_user(){
    const url = `${this.userUrl}/logout`;
    return this.http.post(url,'',{headers:this.headers, withCredentials: true})
      .map((res: Response) => res.json());
  }

  changedata(user: ChangeUser){
    const url = `${this.userUrl}/changeData`;
    return this.http.put(url,JSON.stringify(user),{headers:this.headers})
      .map((res: Response) => res.json());
  }
}
