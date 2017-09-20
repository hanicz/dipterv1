/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter } from '@angular/core';
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

  @Output() closeEvent = new EventEmitter();

  constructor(
    private fileService: FileService
  ){}

  upload(): void {
    this.fileService.upload_file(this.file).subscribe((json: Object) => {
            this.custResp = new CustomResponse().fromJSON(json);
            console.log(this.custResp.Response);
            this.closeEvent.emit();
        },
        error => console.error('Error: ' + error)
        );
  }

  onChange(event: any) {
        this.file = event.srcElement.files;
  }

  close(): void{
    this.closeEvent.emit();
  }
}
