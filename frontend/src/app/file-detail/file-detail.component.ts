/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input } from '@angular/core';
import { File } from '../entities/file';


@Component({
  moduleId: module.id,
  selector: 'file-detail',
  templateUrl: './file-detail.component.html',
  styleUrls: [ './file-detail.component.css' ]
})
export class FileDetailComponent {
    @Input() file: File;
}
