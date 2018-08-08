import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { Travel } from '../entities/travel';
import { DatePipe } from '@angular/common';
import { TravelPlan } from '../entities/travel-plan';
import { map } from "rxjs/operators";

@Injectable()
export class TravelService {

  private headers = new Headers({
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  });

  private userUrl = 'http://localhost:5000/resources/travels';
  //private userUrl = '/resources/travels';


  constructor(
    private http: Http,
    private datePipe: DatePipe) { }


  get_travels() {
    const url = `${this.userUrl}`;
    return this.http.get(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  update_travel(travel: Travel) {
    var data = {
      'description': travel.description,
      'travelDate': this.datePipe.transform(travel.travelDate, 'yyyy-MM-dd'),
      'id': travel.id
    }

    const url = `${this.userUrl}`;
    return this.http.post(url, JSON.stringify(data), {
      headers: this.headers,
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  create_travel(travel: Travel) {
    var data = {
      'description': travel.description,
      'travelDate': this.datePipe.transform(travel.travelDate, 'yyyy-MM-dd')
    }

    const url = `${this.userUrl}`;
    return this.http.put(url, JSON.stringify(data), {
      headers: this.headers,
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  delete_travel(travelId: Number) {
    const url = `${this.userUrl}/${travelId}`;
    return this.http.delete(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  get_travel_plans() {
    const url = `${this.userUrl}/plan`;
    return this.http.get(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  create_travel_plan(plan: TravelPlan) {
    const url = `${this.userUrl}/plan`;
    return this.http.put(url, JSON.stringify(plan), {
      headers: this.headers,
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  update_travel_plan(travel: TravelPlan) {
    const url = `${this.userUrl}/plan`;
    return this.http.post(url, JSON.stringify(travel), {
      headers: this.headers,
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  delete_travel_plan(travelPlanId: Number) {
    const url = `${this.userUrl}/plan/${travelPlanId}`;
    return this.http.delete(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  uploadImage(file: File[], travelId: Number) {
    let headers = new Headers();
    let formData: FormData = new FormData();

     for (let i = 0; i < file.length; i++) {
         formData.append(`files[]`, file[i], file[i].name);
     }

    const url = `${this.userUrl}/image/${travelId}`;
    return this.http.post(url, formData, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }

  get_image_src(travelId: Number){
    const url = `${this.userUrl}/images/${travelId}`;
    return this.http.get(url, {
      withCredentials: true
    }).pipe(
      map((res: Response) => res.json()));
  }
}
