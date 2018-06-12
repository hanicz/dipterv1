/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service'
import { Router } from '@angular/router';
import { ChangeUser } from '../entities/changeuser';
import { FormControl, Validators } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent {

  hidenew = true;
  hideold = true;
  model = new ChangeUser();

  email = new FormControl('', [Validators.pattern('^$|^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$')]);
  password = new FormControl('', [Validators.required]);

  
  constructor(
    private userService: UserService, private router: Router
  ) {
  }

  changeData(): void {
    if (this.email.valid && this.password.valid) {
      this.userService
        .changedata(this.model)
        .subscribe(
          (json: Object) => {
            this.model = new ChangeUser();
          },
          error => console.error('Error: ' + error)
        );
    }
  }
}
