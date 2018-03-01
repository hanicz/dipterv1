import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { Travel } from '../entities/travel';

@Injectable()
export class TravelService {

  private headers = new Headers({
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  });

  private userUrl = 'http://localhost:5000/resources/travels';


  constructor(private http: Http) { }


  get_travels() {
    const url = `${this.userUrl}`;
    return this.http.get(url, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  update_travel(travel: Travel){
    const url = `${this.userUrl}`;
    return this.http.post(url,JSON.stringify(travel), {
      headers: this.headers,
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  create_travel(travel: Travel){
    const url = `${this.userUrl}`;
    return this.http.put(url,JSON.stringify(travel), {
      headers: this.headers,
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  delete_travel(travelId: Number){
    const url = `${this.userUrl}/${travelId}`;
    return this.http.delete(url,{
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }
}
