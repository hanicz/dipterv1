/**
 * Created by Hanicz on 2/21/2017.
 */
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { switchMap } from "rxjs/operators";
import { UserService } from '../services/user.service'
import { CustomResponse } from '../utils/customResponse'

@Component({
  moduleId: module.id,
  selector: 'activate',
  templateUrl: './activate.component.html',
  styleUrls: [ './activate.component.css' ]
})
export class ActivateComponent implements OnInit{
  custResp = new CustomResponse();

  constructor(
    private userService: UserService,
    private route: ActivatedRoute
  ) {
  }

  ngOnInit(): void {
    this.route.params.pipe(
      switchMap((params: Params) => this.userService.activate_user(params['token'])))
      .subscribe(
        (json: Object) => {
          this.custResp = new CustomResponse().fromJSON(json);
          console.log(this.custResp.Response);
        },
        error => {this.custResp.Response = 'Activation failed'}
      );
  }
}
