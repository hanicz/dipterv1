/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit } from '@angular/core';
import { CustomResponse } from '../utils/customResponse';
import { Log } from '../entities/log';
import { NgIf } from '@angular/common';
import { LogService } from '../services/log.service';


@Component({
  moduleId: module.id,
  selector: 'logs',
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.css']
})
export class LogsComponent {

  custResp: CustomResponse;
  logs: Log[];

  constructor(
    private logService: LogService
  ) {
  }

  ngOnInit(): void {
    this.logService.get_logs().subscribe((json: Object[]) => {
      console.log(json);
      this.logs = json as Log[];
    },
      error => console.error('Error: ' + error)
    );
  }
}
