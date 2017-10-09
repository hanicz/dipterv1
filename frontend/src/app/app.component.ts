import { Component } from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  moduleId: module.id,
  selector: 'my-app',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  name = 'Angular';
  menuHidden:boolean;

  constructor(
    private location: Location,
    private router: Router
  ) {
    var pathString = location.path();
    this.menuHidden = !(['/login','/register'].indexOf(location.path()) > -1)
  }

  goToLogs(){
    this.router.navigate(['./logs']);
  }

}
