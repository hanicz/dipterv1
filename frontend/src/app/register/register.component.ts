/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit } from '@angular/core';
import { Headers, Http, URLSearchParams  } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { UserService } from '../services/user.service'
import { User } from '../utils/user'
import { Router } from '@angular/router';

@Component({
  moduleId: module.id,
  selector: 'register',
  templateUrl: './register.component.html',
  styleUrls: [ './register.component.css' ]
})
export class RegisterComponent{

  constructor(
    private userService: UserService,private router: Router
  ){}

  register(): void {
    this.userService
      .register_user(this.model)
      .subscribe(
        (json: Object) => {
            this.model = new User().fromJSON(json);
            console.log(this.model.username);
            this.router.navigate(["/login"]);
        },
        error => console.error('Error: ' + error)
        );
  }

  model = new User();
}
