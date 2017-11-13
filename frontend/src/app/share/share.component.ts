/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { MyFile } from '../entities/file';
import { Role } from '../entities/role';
import { FileShare } from '../entities/FileShare';
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

    @Output() closeEvent = new EventEmitter();
    @Output() changeEvent: EventEmitter<String> = new EventEmitter<String>();

    roles: Role[];
    selectedRole: Role;
    to_user: String;
    shares: FileShare[];

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

    ngOnChanges(changes: SimpleChanges) {
        for (let propName in changes) {
            if (propName == "file" && this.file != undefined) {

                this.shareService.get_shares(this.file.id).subscribe((json: Object) => {
                    console.log(json);
                    this.shares = json as FileShare[];
                },
                    error => console.error('Error: ' + error)
                );
            }
        }
    }

    share(): void {
        this.shareService.shareFile(this.file.id, this.selectedRole.id, this.to_user).subscribe((json: Object) => {
            console.log(json);
            this.to_user = "";
            this.selectedRole = null;
            this.changeEvent.emit("File successfully shared");
        },
            error => {
                console.error('Error: ' + error)
                this.changeEvent.emit("File sharing failed");
            }
        );
    }

    isValid() {
        return this.file.publicLink != null;
    }

    makePublic() {
        this.shareService.makePublic(this.file.id).subscribe((json: Object) => {
            console.log(json);
            this.changeEvent.emit("File made public successfully");
        },
            error => {
                console.error('Error: ' + error)
                this.changeEvent.emit("File public failed");
            }
        );
    }

    revokePublic() {
        this.shareService.revokePublic(this.file.id).subscribe((json: Object) => {
            console.log(json);
            this.changeEvent.emit("File made private successfully");
        },
            error => {
                console.error('Error: ' + error)
                this.changeEvent.emit("File private failed");
            }
        );
    }

    delete_share(share: FileShare): void {
        this.shareService.revoke_share(share.id).subscribe((json: Object) => {
            console.log(json);
            this.shares.splice(this.shares.indexOf(share), 1);
        },
            error => console.error('Error: ' + error)
        );
    }

    close(): void {
        this.closeEvent.emit();
    }
}
