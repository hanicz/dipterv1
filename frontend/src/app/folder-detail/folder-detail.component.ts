/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { Folder } from '../entities/folder';
import { FileService } from '../services/file.service';


@Component({
  moduleId: module.id,
  selector: 'folder-detail',
  templateUrl: './folder-detail.component.html',
  styleUrls: ['./folder-detail.component.css']
})
export class FolderDetailComponent {
  @Input() folder: Folder;

  folders: Folder[]
  moveFolder: Folder;

  @Output() deleteEvent = new EventEmitter();

  constructor(
    private fileService: FileService
  ) { }

  ngOnInit(): void {
    this.fileService.get_folder_list().subscribe((json: Object) => {
      console.log(json);
      this.folders = json as Folder[];
    },
    error => console.error('Error: ' + error)
    );
  }

  isValid() {
    return this.folder.deleted != null;
  }

  rename(): void {
    this.fileService.rename_folder(this.folder).subscribe((json: Object) => {
      console.log(json);
    },
      error => console.error('Error: ' + error)
    );
  }

  delete(): void {
    this.fileService.remove_folder(this.folder.id).subscribe((json: Object) => {
      console.log(json);
      this.folder = null;
      this.deleteEvent.emit();
    },
    error => console.error('Error: ' + error)
    );
  }

  move(): void{
    this.fileService.move_folder(this.folder.id,this.moveFolder.id).subscribe((json: Object) => {
      console.log(json);
    },
    error => console.error('Error: ' + error)
    );
  }
}
