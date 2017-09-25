/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { MyFile } from '../entities/file';
import { Role } from '../entities/role';
import { FileService } from '../services/file.service';
import { RoleService } from '../services/role.service';
import { ShareService } from '../services/share.service';


@Component({
    moduleId: module.id,
    selector: 'notes',
    templateUrl: './notes.component.html',
    styleUrls: ['./notes.component.css']
})
export class NotesComponent {
    @Input() file: MyFile;

    constructor(
        private fileService: FileService,
        private roleService: RoleService,
        private shareService: ShareService
    ) { }
}
