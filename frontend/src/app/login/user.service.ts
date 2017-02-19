/**
 * Created by Hanicy on 2/19/2017.
 */
import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';
import { CustomResponse } from './CustomResponse'

import 'rxjs/add/operator/toPromise';


@Injectable()
export class UserService {

  private headers = new Headers({'Content-Type': 'application/json'});
  private userUrl = 'http://localhost:5000/users';

  constructor(private http: Http) { }

  login_user(): Promise<CustomResponse> {
    const url = `${this.userUrl}/login`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json().data as CustomResponse)
      .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }
}
