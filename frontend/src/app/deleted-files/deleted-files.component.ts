/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit } from '@angular/core';
import { FileService} from '../services/file.service';
import { CustomResponse } from '../utils/customResponse';
import { MyFile } from '../entities/file';
import { Folder } from '../entities/folder';


@Component({
  moduleId: module.id,
  selector: 'deleted-files',
  templateUrl: './deleted-files.component.html',
  styleUrls: [ './deleted-files.component.css' ]
})
export class DeletedFilesComponent {

  custResp: CustomResponse;
  files: MyFile[];
  folders: Folder[];
  selectedFile: MyFile;
  selectedFolder: Folder;

  constructor(
    private fileService: FileService
  ){}

  ngOnInit(): void {
      this.get_deleted_folders();
      this.get_deleted_files();
  }


  get_deleted_files(): void{
    this.fileService.get_deleted_files().subscribe((json: Object) => {
      console.log(json);
      this.files = json as MyFile[];
      },
      error => console.error('Error: ' + error)
      );
  }

  get_deleted_folders(): void{
    this.fileService.get_deleted_folders().subscribe((json: Object) => {
        console.log(json);
        this.folders = json as Folder[];
      },
      error => console.error('Error: ' + error)
      );
  }

  onSelectFile(file: MyFile): void{
    this.selectedFile = file;
  }

  onSelectFolder(folder: Folder): void{
    this.selectedFolder = folder;
  }

  file_restored(): void{
    this.selectedFile = null;
    this.get_deleted_folders();
    this.get_deleted_files();
  }
}
