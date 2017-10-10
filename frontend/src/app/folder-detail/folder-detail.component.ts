/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter } from '@angular/core';
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

  @Output() deleteEvent = new EventEmitter();

  constructor(
    private fileService: FileService
  ) { }

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
}
