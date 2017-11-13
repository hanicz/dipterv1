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
  selector: 'files',
  templateUrl: './files.component.html',
  styleUrls: ['./files.component.css']
})
export class FilesComponent {

  custResp: CustomResponse;
  files: MyFile[];
  folders: Folder[];
  selectedFile: MyFile;
  selectedFolder: Folder;
  currentFolder: Folder;
  search: String;
  requestResponse: String;

  uploadHidden: boolean = true;
  uploadShare: boolean = true;
  createFolderHidden: boolean = true;
  prevent: boolean = false;
  folderHidden: boolean = true;
  fileHidden: boolean = true;
  responseHidden: boolean = true;
  dropboxHidden: boolean = true;

  constructor(
    private fileService: FileService
  ) { }

  ngOnInit(): void {
    this.selectedFolder = new Folder();
    this.selectedFolder.id = 0;
    this.currentFolder = new Folder();
    this.currentFolder.id = 0;
    this.get_folders(this.currentFolder);
    this.get_files(0);
  }


  get_files(folder_id: Number): void {
    this.fileService.get_files(folder_id).subscribe((json: Object) => {
      console.log(json);
      this.files = json as MyFile[];
    },
      error => console.error('Error: ' + error)
    );
  }

  get_folders(folder: Folder): void {
    this.fileService.get_folders(folder.id).subscribe((json: Object) => {
      console.log(json);
      this.folders = json as Folder[];
    },
      error => console.error('Error: ' + error)
    );
  }

  onSelectFile(file: MyFile): void {
    this.selectedFile = file;
    this.fileHidden = false;
    this.folderHidden = true;
  }

  onSelectFolder(folder: Folder): void {
    if (folder.folderName != '...') {
      this.fileHidden = true;
      this.folderHidden = false;
      this.selectedFolder = folder;
    }else{
      this.folderHidden = true;
      this.fileHidden = true;
    }
  }

  onDblSelectFolder(folder: Folder): void {
    this.folderHidden = true;
    this.fileHidden = true;

    this.currentFolder = folder;
    this.get_files(folder.id);
    this.get_folders(folder);
  }

  showUpload(): void {
    this.uploadHidden = false;
  }

  showShare(): void {
    this.uploadShare = false;
  }

  showFolder(): void {
    this.createFolderHidden = false;
  }

  close_upload(): void {
    this.uploadHidden = true;
    this.createFolderHidden = true;
    this.get_files(this.currentFolder.id);
    this.get_folders(this.currentFolder);
  }

  search_files(newValue: String): void {
    this.folderHidden = true;
    this.fileHidden = true;
    this.search = newValue;
    if (newValue == "") {
      this.get_files(this.currentFolder.id);
      this.get_folders(this.currentFolder);
    } else {
      this.fileService.search_files(this.search).subscribe((json: Object) => {
        console.log(json);
        this.files = json as MyFile[];
        this.folders = null;
      },
        error => console.error('Error: ' + error)
      );
    }
  }

  showResponse(event: String){
    this.requestResponse = event;
    this.responseHidden = false;
    setTimeout(() => this.responseHidden = true, 2000);
  }

  showDropbox(event: String){
    this.dropboxHidden = false;
  }
}
