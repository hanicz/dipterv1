
import { FileService } from '../services/file.service';
import { CustomResponse } from '../utils/customResponse';
import { Folder } from '../entities/folder';
import { Component, OnInit, Inject, ViewChild } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { DropboxService } from '../services/dropbox.service';

@Component({
  moduleId: module.id,
  selector: 'upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent {

  custResp: CustomResponse;
  file: File[];
  folder: Number;
  newFolder: Folder;
  path: String;
  filename: String;

  @ViewChild('filePicker') filePicker: any;

  constructor(
    private fileService: FileService,
    private dropboxService: DropboxService,
    public dialogRef: MatDialogRef<UploadComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) {
    this.folder = data.folderId;
    this.newFolder = new Folder();
    this.path = "/"
  }

  upload(): void {
    this.fileService.upload_file(this.file, this.folder).subscribe((json: Object) => {
      this.custResp = new CustomResponse().fromJSON(json);
      console.log(this.custResp.Response);
      this.filePicker.nativeElement.value = "";
    },
      error => console.error('Error: ' + error)
    );
  }

  createFolder(): void {
    this.newFolder.parent = this.folder;
    this.fileService.create_folder(this.newFolder).subscribe((json: Object) => {
      console.log(json);
      this.newFolder = new Folder();
      this.dialogRef.close();
    },
      error => console.error('Error: ' + error)
    );
  }
  download() {
    this.dropboxService.download_from_dropbox(this.path, this.filename, this.folder).subscribe((json: Object) => {
      console.log(json);
      this.path = "/";
      this.filename = "";
      this.dialogRef.close();
    },
      error => {
        console.error('Error: ' + error)
      }
    );
  }

  onChange(event: any) {
    this.file = event.srcElement.files;
  }
}
