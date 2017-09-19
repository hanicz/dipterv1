/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit } from '@angular/core';
import { FileService} from '../services/file.service';
import { CustomResponse } from '../utils/customResponse';
import { File } from '../entities/file';
import { Folder } from '../entities/folder';


@Component({
  moduleId: module.id,
  selector: 'files',
  templateUrl: './files.component.html',
  styleUrls: [ './files.component.css' ]
})
export class FilesComponent {

  custResp: CustomResponse;
  files: File[];
  folders: Folder[];
  selectedFile: File;
  selectedFolder: Folder;

  constructor(
    private fileService: FileService
  ){}

  ngOnInit(): void {
      this.get_files(0);
      this.get_folders(0);
  }


  get_files(folder_id: number): void{
    this.fileService.get_files(folder_id).subscribe((json: Object) => {
      console.log(json);
      this.files = json as File[];
      },
      error => console.error('Error: ' + error)
      );
  }

  get_folders(folder_id: number): void{
    this.fileService.get_folders(folder_id).subscribe((json: Object) => {
      console.log(json);
      this.folders = json as Folder[];
      },
      error => console.error('Error: ' + error)
      );
  }

  onSelectFile(file: File): void{
    this.selectedFile = file;
  }

  onSelectFolder(folder: Folder): void{
    this.selectedFolder = folder;
  }
}
