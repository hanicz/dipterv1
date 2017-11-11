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
    notesShare: boolean = true;
    requestResponse: String;
    responseHidden: boolean = true;

    constructor(
        private fileService: FileService,
        private roleService: RoleService,
        private noteService: NoteService
    ) { }

    ngOnInit(): void {
        this.selectedNote = new MyFile();

        this.noteService.get_notes().subscribe((json: Object) => {
            console.log(json);
            this.notes = json as MyFile[];
        },
            error => console.error('Error: ' + error)
        );
    }

    onSelectNote(note: MyFile): void {
        this.selectedNote = note;
    }

    isValid() {
        return this.selectedNote.created != null;
    }

    update_note(): void {
        this.noteService.update_note(this.selectedNote).subscribe((json: Object) => {
            console.log(json);
            this.showResponse("Note updated successfully");
        },
            error => {
                console.error('Error: ' + error);
                this.showResponse("Note update failed");
            }
        );
    }

    delete_note(): void {
        this.noteService.delete_note(this.selectedNote.id).subscribe((json: Object) => {
            console.log(json);
            this.notes.splice(this.notes.indexOf(this.selectedNote), 1);
            this.selectedNote = new MyFile();
            this.showResponse("Note deleted successfully");
        },
            error => {
                console.error('Error: ' + error);
                this.showResponse("Note delete failed");
            }
        );
    }

    new_note(): void {

        if (this.isValid()) {
            this.selectedNote = new MyFile();
        } else {

            this.noteService.new_note(this.selectedNote).subscribe((json: Object) => {
                console.log(json);
                this.notes.push(json as MyFile);
                this.showResponse("Note created successfully");
                this.selectedNote = new MyFile();
            },
                error => {
                    console.error('Error: ' + error);
                    this.showResponse("Note creation failed");
                }
            );
        }
    }

    showShare(): void {
        this.notesShare = false;
    }

    showResponse(event: String) {
        this.requestResponse = event;
        this.responseHidden = false;
        setTimeout(() => this.responseHidden = true, 1500);
    }
}
