/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component } from '@angular/core';
import { Router } from '@angular/router'
import { UserService } from '../services/user.service'
import { CustomResponse } from '../utils/customResponse'
import { User } from '../utils/user'

@Component({
  moduleId: module.id,
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  model = new User();
  custResp: CustomResponse;

  constructor(
    private userService: UserService,
    private router: Router
  ) { }

  login(): void {
    this.userService
      .login_user(this.model)
      .subscribe(
      (json: Object) => {
        this.custResp = new CustomResponse().fromJSON(json);
        console.log(this.custResp.Response);
        this.router.navigate(['./files']);
      },
      error => {
        console.error('Error: ' + error);
        console.log(this.router.url);
      }
      );
  }
}
