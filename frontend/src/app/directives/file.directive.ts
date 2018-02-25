import {Directive, HostListener, HostBinding, Input} from '@angular/core';
import { FileService } from '../services/file.service';

@Directive({
  selector: '[appFile]'
})
export class FileDirective {

  @Input() currentFolder: Number;

  constructor(private fileService: FileService) { }

  @HostListener('dragover', ['$event']) public onDragOver(evt){
    evt.preventDefault();
    evt.stopPropagation();
  }
  @HostListener('dragleave', ['$event']) public onDragLeave(evt){
    evt.preventDefault();
    evt.stopPropagation();
  }

  @HostListener('drop', ['$event']) public onDrop(evt){
    
    evt.preventDefault();
    evt.stopPropagation();
    let files = evt.dataTransfer.files;
    if(files.length > 0){
      this.fileService.upload_file(files, this.currentFolder).subscribe((json: Object) => {
        console.log(json);
      },
        error => console.error('Error: ' + error)
      );
    }
  }

}
