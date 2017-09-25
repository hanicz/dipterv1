/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable }    from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { CustomResponse } from '../utils/customResponse'

import 'rxjs/add/operator/map';



@Injectable()
export class RoleService {

  private headers = new Headers({'Content-Type': 'multipart/form-data',
                                  'Accept': 'application/json'});
  private userUrl = 'http://localhost:5000/roles';

  constructor(private http: Http) { }

  get_roles(){
    const url = `${this.userUrl}/getAllRoles`;
    return this.http.get(url,{
        withCredentials: true
      })
      .map((res: Response) => res.json());
  }

}
