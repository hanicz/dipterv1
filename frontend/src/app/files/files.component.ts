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
  selector: 'files',
  templateUrl: './files.component.html',
  styleUrls: [ './files.component.css' ]
})
export class FilesComponent {

  custResp: CustomResponse;
  files: MyFile[];
  folders: Folder[];
  selectedFile: MyFile;
  selectedFolder: Folder;
  currentFolder: Folder;
  uploadHidden:boolean = true;
  uploadShare:boolean = true;
  prevent:boolean = false;
  delay:number = 0;

  constructor(
    private fileService: FileService
  ){}

  ngOnInit(): void {
      this.get_folders(0);
      this.get_files(0);
  }


  get_files(folder_id: Number): void{
    this.fileService.get_files(folder_id).subscribe((json: Object) => {
      console.log(json);
      this.files = json as MyFile[];
      },
      error => console.error('Error: ' + error)
      );
  }

  get_folders(folder_id: Number): void{
    this.fileService.get_folders(folder_id).subscribe((json: Object) => {
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

  onDblSelectFolder(folder: Folder): void{
    this.currentFolder = folder;
    this.get_files(folder.id);
    this.get_folders(folder.id);
  }

  showUpload(): void{
    this.uploadHidden = false;
  }

  showShare(): void{
    this.uploadShare = false;
  }
}
