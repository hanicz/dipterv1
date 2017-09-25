/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { MyFile } from '../entities/file';
import { Role } from '../entities/role';
import { FileService } from '../services/file.service';
import { RoleService } from '../services/role.service';
import { ShareService } from '../services/share.service';


@Component({
    moduleId: module.id,
    selector: 'share',
    templateUrl: './share.component.html',
    styleUrls: ['./share.component.css']
})
export class ShareComponent {
    @Input() file: MyFile;

    roles: Role[];
    selectedRole: Role;
    to_user: String;

    constructor(
        private fileService: FileService,
        private roleService: RoleService,
        private shareService: ShareService
    ) { }

    ngOnInit(): void {
        this.roleService.get_roles().subscribe((json: Object) => {
            console.log(json);
            this.roles = json as Role[];
        },
            error => console.error('Error: ' + error)
        );
    }

    share(): void {
        this.shareService.shareFile(this.file.id,this.selectedRole.id,this.to_user).subscribe((json: Object) => {
            console.log(json);
            this.to_user = "";
            this.selectedRole = null;
        },
            error => console.error('Error: ' + error)
        );
    }

    isValid() {
        return this.file.publicLink != null;
    }

    makePublic(){
        this.shareService.makePublic(this.file.id).subscribe((json: Object) => {
            console.log(json);
        },
            error => console.error('Error: ' + error)
        );
    }

    revokePublic(){
        this.shareService.revokePublic(this.file.id).subscribe((json: Object) => {
            console.log(json);
        },
            error => console.error('Error: ' + error)
        );
    }
}
