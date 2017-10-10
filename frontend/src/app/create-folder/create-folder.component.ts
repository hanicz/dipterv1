/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { FileService } from '../services/file.service';
import { CustomResponse } from '../utils/customResponse';
import { Folder } from '../entities/folder'

@Component({
    moduleId: module.id,
    selector: 'create-folder',
    templateUrl: './create-folder.component.html',
    styleUrls: ['./create-folder.component.css']
})
export class CreateFolderComponent {

    custResp: CustomResponse;
    newFolder: Folder;

    @Input() folder: Number;
    @Output() closeEvent = new EventEmitter();

    constructor(
        private fileService: FileService
    ) { 
        this.newFolder = new Folder();
    }

    create(): void {
        this.newFolder.parent = this.folder;
        this.fileService.create_folder(this.newFolder).subscribe((json: Object) => {
            console.log(json);
            this.closeEvent.emit();
        },
            error => console.error('Error: ' + error)
        );
    }

    close(): void {
        this.closeEvent.emit();
    }
}
