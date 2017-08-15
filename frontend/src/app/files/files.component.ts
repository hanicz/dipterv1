/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit } from '@angular/core';
import { FileService} from '../services/file.service';
import { CustomResponse } from '../utils/customResponse';
import { File } from '../entities/file';

@Component({
  moduleId: module.id,
  selector: 'upload',
  templateUrl: './upload.component.html',
  styleUrls: [ './upload.component.css' ]
})
export class FilesComponent {

  custResp: CustomResponse;
  file: File[];

  constructor(
    private fileService: FileService
  ){}

  ngOnInit(): void {
      this.fileService.get_files(0).subscribe((json: Object) => {
            console.log(json);
        },
        error => console.error('Error: ' + error)
        );
  }

  onChange(event: any) {
        this.file = event.srcElement.files;
    }
}
