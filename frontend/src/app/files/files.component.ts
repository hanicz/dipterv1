/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, OnInit } from '@angular/core';
import { FileService} from '../services/file.service';
import { CustomResponse } from '../utils/customResponse';
import { File } from '../entities/file';

const FILES: File[] = [
  { id: 11, name: 'Test1' },
  { id: 12, name: 'Test2' },
  { id: 13, name: 'Test3' },
];

@Component({
  moduleId: module.id,
  selector: 'files',
  templateUrl: './files.component.html',
  styleUrls: [ './files.component.css' ]
})
export class FilesComponent {

  custResp: CustomResponse;
  file: File[];
  files = FILES;

  constructor(
    private fileService: FileService
  ){}

  ngOnInit(): void {
   /*   this.fileService.get_files(0).subscribe((json: Object) => {
            console.log(json);
        },
        error => console.error('Error: ' + error)
        );*/
  }

  onChange(event: any) {
        this.file = event.srcElement.files;
    }
}
