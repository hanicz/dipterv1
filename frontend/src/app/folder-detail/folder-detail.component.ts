/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input } from '@angular/core';
import { Folder } from '../entities/folder';


@Component({
  moduleId: module.id,
  selector: 'folder-detail',
  templateUrl: './folder-detail.component.html',
  styleUrls: [ './folder-detail.component.css' ]
})
export class FolderDetailComponent {
    @Input() folder: Folder;
}
