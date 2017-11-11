/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { MyFile } from '../entities/file';
import { Folder } from '../entities/folder';
import { FileService } from '../services/file.service';
import { LogService } from '../services/log.service';
import { Log } from '../entities/log';
import { DropboxService } from '../services/dropbox.service';
import saveAs = require('file-saver');

@Component({
  moduleId: module.id,
  selector: 'file-detail',
  templateUrl: './file-detail.component.html',
  styleUrls: ['./file-detail.component.css']
})
export class FileDetailComponent {
  @Input() file: MyFile;

  folders: Folder[]
  moveFolder: Folder;
  logs: Log[];

  @Output() shareEvent = new EventEmitter();
  @Output() changeEvent: EventEmitter<String> = new EventEmitter<String>();

  constructor(
    private fileService: FileService,
    private logService: LogService,
    private dropboxService: DropboxService
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
      if (propName == "file" && this.file != undefined) {

        this.logService.get_file_logs(this.file.id).subscribe((json: Object) => {
          console.log(json);
          this.logs = json as Log[];
        },
          error => console.error('Error: ' + error)
        );
      }
    }
  }

  rename(): void {
    this.fileService.rename_file(this.file).subscribe((json: Object) => {
      console.log(json);
      this.changeEvent.emit("File renamed successfully");
    },
      error => {
        console.error('Error: ' + error)
        this.changeEvent.emit("File rename failed");
      }
    );
  }

  delete(): void {
    this.fileService.remove_file(this.file.id).subscribe((json: Object) => {
      console.log(json);
      this.file = null;
      this.changeEvent.emit("File deleted successfully");
    },
      error => {
        console.error('Error: ' + error)
        this.changeEvent.emit("File delete failed");
      }
    );
  }

  isValid() {
    return this.file.deleted != null;
  }

  share(): void {
    this.shareEvent.emit();
  }

  move(): void {
    this.fileService.move_file(this.moveFolder.id, this.file.id).subscribe((json: Object) => {
      console.log(json);
      this.changeEvent.emit("File moved successfully");
    },
      error => {
        console.error('Error: ' + error)
        this.changeEvent.emit("File move failed");
      }
    );
  }

  restore(): void {
    this.fileService.restore_file(this.file.id).subscribe((json: Object) => {
      console.log(json);
      this.changeEvent.emit("File restored successfully");
    },
      error => {
        console.error('Error: ' + error)
        this.changeEvent.emit("File restore failed");
      }
    );
  }

  dropbox(): void {
    this.dropboxService.upload_to_dropbox(this.file.id).subscribe((json: Object) => {
      console.log(json);
      this.changeEvent.emit("File uploaded to dropbox successfully");
    },
      error => {
        console.error('Error: ' + error)
        this.changeEvent.emit("File upload to dropbox failed");
      }
    );
  }

  download(): void {

    var newWindow = window.open('http://localhost:5000/files/download/' + this.file.id);

    /*this.fileService.download(this.file.id).subscribe(blob => {
      this.changeEvent.emit("File download started successfully");
      saveAs(blob, this.file.fileName.toString());
    });*/
  }
}
