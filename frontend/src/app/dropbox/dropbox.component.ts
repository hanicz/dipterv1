/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit } from '@angular/core';
import { DropboxService } from '../services/dropbox.service'


@Component({
  moduleId: module.id,
  selector: 'dropbox',
  templateUrl: './dropbox.component.html',
  styleUrls: ['./dropbox.component.css']
})
export class DropboxComponent {

    url: String;
    token: String;

  constructor(
      private dropboxService: DropboxService
  ) { }


  ngOnInit(): void {
    this.dropboxService.get_url().subscribe((json: Object) => {
      this.url = JSON.parse(JSON.stringify(json)).url;
    },
    error => console.error('Error: ' + error)
    );
  }

  finish_auth(): void{
    this.dropboxService.finish_auth(this.token).subscribe((json: Object) => {
      },
      error => console.error('Error: ' + error)
      );
  }
}
