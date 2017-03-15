/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component } from '@angular/core';
import { FileService} from '../services/file.service';
import { CustomResponse } from '../utils/customResponse';

@Component({
  moduleId: module.id,
  selector: 'upload',
  templateUrl: './upload.component.html',
  styleUrls: [ './upload.component.css' ]
})
export class UploadComponent {

  custResp: CustomResponse;
  file: File[];

  constructor(
    private fileService: FileService
  ){}

  upload(): void {
    this.fileService.upload_file(this.file).subscribe((json: Object) => {
            this.custResp = new CustomResponse().fromJSON(json);
            console.log(this.custResp.Response);
        },
        error => console.error('Error: ' + error)
        );
  }

  onChange(event: any) {
        this.file = event.srcElement.files;
    }
}
