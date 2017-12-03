/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit } from '@angular/core';
import { Headers, Http, URLSearchParams  } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { UserService } from '../services/user.service'
import { Router } from '@angular/router';
import { ChangeUser } from '../entities/changeuser'
import { CustomResponse } from '../utils/customResponse'

@Component({
  moduleId: module.id,
  selector: 'settings',
  templateUrl: './settings.component.html',
  styleUrls: [ './settings.component.css' ]
})
export class SettingsComponent{

  model = new ChangeUser();

  constructor(
    private userService: UserService,private router: Router
  ){
  }

  changeData(): void {
    this.userService
      .changedata(this.model)
      .subscribe(
        (json: Object) => {
            console.log(new CustomResponse().fromJSON(json).Response);
        },
        error => console.error('Error: ' + error)
        );
  }
}
