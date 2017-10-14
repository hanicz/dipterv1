/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { Folder } from '../entities/folder';
import { FileService } from '../services/file.service';
import { LogService } from '../services/log.service';
import { Log } from '../entities/log';


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
  logs: Log[];

  @Output() deleteEvent = new EventEmitter();

  constructor(
    private fileService: FileService,
    private logService: LogService
  ) { }

  ngOnInit(): void {
    this.fileService.get_folder_list().subscribe((json: Object) => {
      console.log(json);
      this.folders = json as Folder[];
    },
    error => console.error('Error: ' + error)
    );
  }

  ngOnChanges(changes: SimpleChanges) {
    for (let propName in changes) {
        if (propName == "folder" && this.folder != undefined) {

          this.logService.get_folder_logs(this.folder.id).subscribe((json:Object) => {
            console.log(json);
            this.logs = json as Log[];
          },
          error => console.error('Error: ' + error)
          );
        }
    }
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
