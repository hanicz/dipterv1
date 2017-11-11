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

  @Output() changeEvent: EventEmitter<String> = new EventEmitter<String>();

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

        this.logService.get_folder_logs(this.folder.id).subscribe((json: Object) => {
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
      this.changeEvent.emit("Folder renamed successfully");
    },
      error => {
        console.error('Error: ' + error)
        this.changeEvent.emit("Folder rename failed");
      }
    );
  }

  delete(): void {
    this.fileService.remove_folder(this.folder.id).subscribe((json: Object) => {
      console.log(json);
      this.folder = null;
      this.changeEvent.emit("Folder deleted successfully");
    },
      error => {
        console.error('Error: ' + error)
        this.changeEvent.emit("Folder delete failed");
      }
    );
  }

  move(): void {
    this.fileService.move_folder(this.folder.id, this.moveFolder.id).subscribe((json: Object) => {
      console.log(json);
      this.changeEvent.emit("Folder moved successfully");
    },
      error => {
        console.error('Error: ' + error)
        this.changeEvent.emit("Folder move failed");
      }
    );
  }

  restore(): void {
    this.fileService.restore_folder(this.folder.id).subscribe((json: Object) => {
      console.log(json);
      this.changeEvent.emit("Folder restored successfully");
    },
      error => {
        console.error('Error: ' + error)
        this.changeEvent.emit("Folder restore failed");
      }
    );
  }

  download(): void {
    
        var newWindow = window.open('http://localhost:5000/files/download/folder/' + this.folder.id);
    
        /*this.fileService.download(this.file.id).subscribe(blob => {
          this.changeEvent.emit("File download started successfully");
          saveAs(blob, this.file.fileName.toString());
        });*/
      }
}
