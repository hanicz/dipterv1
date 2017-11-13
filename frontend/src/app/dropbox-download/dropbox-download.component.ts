/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, Output, EventEmitter} from '@angular/core';
import { Folder } from '../entities/folder';
import { Role } from '../entities/role';
import { FileShare } from '../entities/FileShare';
import { DropboxService } from '../services/dropbox.service';
import { RoleService } from '../services/role.service';
import { ShareService } from '../services/share.service';


@Component({
    moduleId: module.id,
    selector: 'dropbox-download',
    templateUrl: './dropbox-download.component.html',
    styleUrls: ['./dropbox-download.component.css']
})
export class DropboxDownloadComponent {
    @Input() folder: Folder;

    path: String;
    filename: String;

    @Output() closeEvent= new EventEmitter();
    @Output() downloadEvent: EventEmitter<String> = new EventEmitter<String>();

    constructor(
        private dropboxService: DropboxService
    ) {
        this.path = "/"
     }

    download() {
        this.dropboxService.download_from_dropbox(this.path,this.filename,this.folder.id).subscribe((json: Object) => {
            console.log(json);
            this.path = "/";
            this.filename = "";
            this.downloadEvent.emit("File download started successfully");
        },
        error => {
            console.error('Error: ' + error)
            this.downloadEvent.emit("File download failed");
          }
        );
    }

    close(): void{
        this.closeEvent.emit();
    }
}
