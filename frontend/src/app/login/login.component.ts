import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router'
import { UserService } from '../services/user.service'
import { CustomResponse } from '../utils/customResponse'
import { User } from '../utils/user'
import { FormControl, Validators } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  hide = true;

  user = new User();
  custResp: CustomResponse;

  username = new FormControl('', [Validators.required]);
  password = new FormControl('', [Validators.required]);

  constructor(
    private userService: UserService,
    private router: Router
  ) { }

  ngOnInit() {
  }

  login(): void {

    if (this.username.valid && this.password.valid) {

      this.userService
        .login_user(this.user)
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
}
