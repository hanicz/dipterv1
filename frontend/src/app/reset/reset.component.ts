/**
 * Created by Hanicz on 2/21/2017.
 */
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { UserService } from '../services/user.service'
import { CustomResponse } from '../utils/customResponse'
import { ResetUser } from '../entities/reset-user'

@Component({
  moduleId: module.id,
  selector: 'reset',
  templateUrl: './reset.component.html',
  styleUrls: [ './reset.component.css' ]
})
export class ResetComponent implements OnInit{
  custResp = new CustomResponse();
  model = new ResetUser();

  constructor(
    private userService: UserService,
    private route: ActivatedRoute,
    private router: Router
  ) {
  }

  ngOnInit(): void {
      this.route.params.subscribe((params: Params) => this.model.token = params['token']);
  }

  reset_user(){
    this.userService.reset_user(this.model)
      .subscribe(
        (json: Object) => {
          this.custResp = new CustomResponse().fromJSON(json);
          this.router.navigate(['/login'])
        },
        error => {this.custResp.Response = 'Activation failed'}
      );
  }
}
