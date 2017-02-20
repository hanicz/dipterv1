/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit } from '@angular/core';
import { Headers, Http, URLSearchParams  } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { UserService } from '../services/user.service'
import { User } from '../utils/user'

@Component({
  moduleId: module.id,
  selector: 'register',
  templateUrl: './register.component.html',
  styleUrls: [ './register.component.css' ]
})
export class RegisterComponent{

  user: User;

  constructor(
    private userService: UserService
  ){}

  register(username: string, password: string, email: string): void {
    this.userService
      .regist_user(username,password,email)
      .subscribe(
        (json: Object) => {
            this.user = new User().fromJSON(json);
            console.log(this.user.name);
        },
        error => console.error('Error: ' + error)
        );
  }

}
