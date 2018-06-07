/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit, HostListener } from '@angular/core';
import { Headers, Http, URLSearchParams } from '@angular/http';
import { UserService } from '../services/user.service'
import { User } from '../utils/user'
import { Router } from '@angular/router';
import { FormControl, Validators } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {

  hide = true;

  user = new User();

  email = new FormControl('', [Validators.required, Validators.email]);
  password = new FormControl('', [Validators.required]);
  username = new FormControl('', [Validators.required]);

  constructor(
    private userService: UserService, private router: Router
  ) { }

  @HostListener('window:keydown', ['$event'])
  keyboardInput(event: KeyboardEvent) {
    if(event.keyCode == 13){
      this.register();
    }
  }

  register(): void {
    if (this.username.valid && this.password.valid && this.email.valid) {
      this.userService
        .register_user(this.user)
        .subscribe(
          (json: Object) => {
            this.user = json as User;
            console.log(this.user.username);
            this.router.navigate(["/login"]);
          },
          error => console.error('Error: ' + error)
        );
    }
  }
}
