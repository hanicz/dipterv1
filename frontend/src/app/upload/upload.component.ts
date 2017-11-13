/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter, ViewChild  } from '@angular/core';
import { FileService} from '../services/file.service';
import { CustomResponse } from '../utils/customResponse';
import { Folder } from '../entities/folder'

@Component({
  moduleId: module.id,
  selector: 'upload',
  templateUrl: './upload.component.html',
  styleUrls: [ './upload.component.css' ]
})
export class UploadComponent {

  custResp: CustomResponse;
  file: File[];

  @Input() folder: Number;
  @Output() closeEvent = new EventEmitter();

  @ViewChild('filePicker') filePicker: any;

  constructor(
    private fileService: FileService
  ){}

  upload(): void {
    this.fileService.upload_file(this.file,this.folder).subscribe((json: Object) => {
            this.custResp = new CustomResponse().fromJSON(json);
            console.log(this.custResp.Response);
            this.filePicker.nativeElement.value = "";
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
