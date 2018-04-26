/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { CustomResponse } from '../utils/customResponse'

import 'rxjs/add/operator/map';



@Injectable()
export class RoleService {

  private headers = new Headers({
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  });

  //private userUrl = 'http://localhost:5000/resources/roles';
  private userUrl = '/resources/roles';

  constructor(private http: Http) { }

  get_roles() {
    const url = `${this.userUrl}`;
    return this.http.get(url, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

}
