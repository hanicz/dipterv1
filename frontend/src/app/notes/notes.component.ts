/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, EventEmitter, OnInit } from '@angular/core';
import { MyFile } from '../entities/file';
import { FileService } from '../services/file.service';
import { RoleService } from '../services/role.service';
import { NoteService } from '../services/note.service';


@Component({
    moduleId: module.id,
    selector: 'notes',
    templateUrl: './notes.component.html',
    styleUrls: ['./notes.component.css']
})
export class NotesComponent {

    notes: MyFile[];
    selectedNote: MyFile;

    constructor(
        private fileService: FileService,
        private roleService: RoleService,
        private noteService: NoteService
    ) { }

    ngOnInit(): void {
        this.selectedNote = new MyFile();

        this.noteService.get_files().subscribe((json: Object) => {
            console.log(json);
            this.notes = json as MyFile[];
        },
            error => console.error('Error: ' + error)
        );
    }

    onSelectNote(note: MyFile): void{
        this.selectedNote = note;
    }
}
