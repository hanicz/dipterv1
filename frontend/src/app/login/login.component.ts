/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component } from '@angular/core';
import { Headers, Http, URLSearchParams  } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { UserService } from '../services/user.service'
import { CustomResponse } from '../utils/customResponse'

@Component({
  moduleId: module.id,
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: [ './login.component.css' ]
})
export class LoginComponent {

  custResp: CustomResponse;

  constructor(
    private userService: UserService
  ){}

  login(username: string, password: string): void {
    this.userService
      .login_user(username,password)
      .subscribe(
        (json: Object) => {
            this.custResp = new CustomResponse().fromJSON(json);
            console.log(this.custResp.Response);
        },
        error => console.error('Error: ' + error)
        );
  }
}
