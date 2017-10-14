/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { MyFile } from '../entities/file';
import { Folder } from '../entities/folder';
import { FileService } from '../services/file.service';
import { LogService } from '../services/log.service';
import { Log } from '../entities/log';


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


  @Output() deleteEvent = new EventEmitter();
  @Output() shareEvent = new EventEmitter();

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
        if (propName == "file" && this.file != undefined) {

          this.logService.get_file_logs(this.file.id).subscribe((json:Object) => {
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
    },
    error => console.error('Error: ' + error)
    );
  }

  delete(): void {
    this.fileService.remove_file(this.file.id).subscribe((json: Object) => {
      console.log(json);
      this.file = null;
      this.deleteEvent.emit();
    },
    error => console.error('Error: ' + error)
    );
  }

  isValid() {
    return this.file.deleted != null;
  }

  share(): void{
    this.shareEvent.emit();
  }

  move(): void{
    this.fileService.move_file(this.moveFolder.id,this.file.id).subscribe((json: Object) => {
      console.log(json);
    },
    error => console.error('Error: ' + error)
    );
  }

  restore(): void{
    this.fileService.restore_file(this.file.id).subscribe((json:Object) => {
      console.log(json);
      this.deleteEvent.emit();
    },
    error => console.error('Error: ' + error)
    );
  }
}
