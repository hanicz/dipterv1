/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { MyFile } from '../entities/file';
import { FileService } from '../services/file.service';


@Component({
  moduleId: module.id,
  selector: 'file-detail',
  templateUrl: './file-detail.component.html',
  styleUrls: ['./file-detail.component.css']
})
export class FileDetailComponent {
  @Input() file: MyFile;

  @Output() deleteEvent = new EventEmitter();

  constructor(
    private fileService: FileService
  ) { }

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

  restore_file(){
    
  }
}
