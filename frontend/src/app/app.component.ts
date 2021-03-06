import { Component } from '@angular/core';
import { Location } from '@angular/common';
import { Router, NavigationEnd } from '@angular/router';
import 'hammerjs';
import { UserService } from './services/user.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  name = 'Hanicz';
  menuHidden:boolean;
  notemenuitems = [
    {text: 'My notes', icon: 'far fa-sticky-note', router: 'notes'},
    {text: 'Shared with me', icon: 'far fa-handshake', router: 'shared-notes'}
  ];

  filemenuitems = [
    {text: 'My files', icon: 'far fa-file', router: 'files'},
    {text: 'Shared with me', icon: 'far fa-handshake', router: 'shared-with-me'},
    {text: 'Deleted files', icon: 'far fa-trash-alt', router: 'deleted-files'}
  ];

  usermenuitems = [
    {text: 'Change data', icon: 'fas fa-wrench', router: 'settings'},
    {text: 'Dropbox', icon: 'fab fa-dropbox', router: 'dropbox'},
    {text: 'Logs', icon: 'fas fa-angle-right', router: 'logs'},
    {text: 'Logout', icon: 'fas fa-sign-out-alt', router: 'logout'},
    {text: 'Delete account', icon: 'fas fa-trash-alt', router: 'delete'}
  ];

  financemenuitems = [
    {text: 'Chart', icon: 'fas fa-chart-pie', router: 'finance-chart'},
    {text: 'Table', icon: 'far fa-money-bill-alt', router: 'finance'}
  ];

  travelmenuitems = [
    {text: 'Travels', icon: 'far fa-map', router: 'travel'},
    {text: 'Images', icon: 'far fa-images', router: 'travel-images'},
    {text: 'Plans', icon: 'fas fa-map-marker', router: 'travel-plan'}
  ];

  selectedList = [];

  constructor(
    private location: Location,
    private router: Router,
    private userService: UserService
  ) {
    this.router.events.subscribe((event) => {
      if(event instanceof NavigationEnd){
        var pathString = location.path();
        this.menuHidden = !(['/login','/register'].indexOf(location.path()) > -1);
        if((['/files','/shared-with-me', '/deleted-files'].indexOf(location.path()) > -1)) this.selectedList = this.filemenuitems;
        else if((['/notes','/shared-notes'].indexOf(location.path()) > -1)) this.selectedList = this.notemenuitems;
        else if((['/settings','/dropbox', '/logs'].indexOf(location.path()) > -1)) this.selectedList = this.usermenuitems;
        else if((['/finance','/finance-chart'].indexOf(location.path()) > -1)) this.selectedList = this.financemenuitems;
        else if((['/travel','/travel-plan', '/travel-images'].indexOf(location.path()) > -1)) this.selectedList = this.travelmenuitems;
        else this.selectedList = [];
      }
  });
  }

  logout(): void{
    this.userService
    .logout().subscribe((json: Object) => {
      this.router.navigate(['./login']);
    },
    error => {
      console.error('Error: ' + error);
    }
    );
  }

  clickMenuItem(routeString){
    if(routeString == 'logout') this.logout();
    else if(routeString == 'delete') this.delete();
    else this.router.navigate(['./' + routeString]);
  }

  delete(): void{
    var del = window.confirm('Are you sure you want to delete your account?')
    if (del == true) {
      this.userService
      .delete().subscribe((json: Object) => {
        this.router.navigate(['./login']);
      },
      error => {
        console.error('Error: ' + error);
      }
      );
    }
  }
}
