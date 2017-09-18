/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable }    from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { CustomResponse } from '../utils/customResponse'

import 'rxjs/add/operator/map';



@Injectable()
export class LogService {

  private headers = new Headers({'Content-Type': 'multipart/form-data',
                                  'Accept': 'application/json'});
  private userUrl = 'http://localhost:5000/logs';

  constructor(private http: Http) { }

  get_logs(){
    const url = `${this.userUrl}/log`;
    return this.http.get(url,{
        withCredentials: true
      })
      .map((res: Response) => res.json());
  }

}
