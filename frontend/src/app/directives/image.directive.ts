import {Directive, HostListener, HostBinding, Input} from '@angular/core';
import { TravelService } from '../services/travel.service';

@Directive({
  selector: '[appImage]'
})
export class ImageDirective {

  @Input() currentTravel: Number;

  constructor(private travelService: TravelService) { }

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
      this.travelService.uploadImage(files, this.currentTravel).subscribe((json: Object) => {
        console.log(json);
      },
        error => console.error('Error: ' + error)
      );
    }
  }

}
