/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit } from '@angular/core';
import { FileService } from '../services/file.service';
import { CustomResponse } from '../utils/customResponse';
import { MyFile } from '../entities/file';
import { Folder } from '../entities/folder';


@Component({
  moduleId: module.id,
  selector: 'shared-with-me',
  templateUrl: './shared-with-me.component.html',
  styleUrls: ['./shared-with-me.component.css']
})
export class SharedWithMeComponent {

    files: MyFile[];
    fileHidden: boolean = true;
    selectedFile: MyFile;

  constructor(
    private fileService: FileService
  ) { }

  ngOnInit(): void {
    this.fileService.get_shared_with_me_files().subscribe((json: Object) => {
        console.log(json);
        this.files = json as MyFile[];
      },
        error => console.error('Error: ' + error)
      );
  }

  onSelectFile(file: MyFile): void {
    this.fileHidden = false;
    this.selectedFile = file;
  }
}
