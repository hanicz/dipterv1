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

  constructor(
    private userService: UserService
  ){}

  register(): void {
    this.userService
      .regist_user(this.model)
      .subscribe(
        (json: Object) => {
            this.model = new User("","","").fromJSON(json);
            console.log(this.model.username);
        },
        error => console.error('Error: ' + error)
        );
  }

  model = new User('','','');
}
