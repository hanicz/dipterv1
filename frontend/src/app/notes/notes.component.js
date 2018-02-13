"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * Created by Hanicz on 2/19/2017.
 */
var core_1 = require("@angular/core");
var file_1 = require("../entities/file");
var file_service_1 = require("../services/file.service");
var role_service_1 = require("../services/role.service");
var note_service_1 = require("../services/note.service");
var NotesComponent = /** @class */ (function () {
    function NotesComponent(fileService, roleService, noteService) {
        this.fileService = fileService;
        this.roleService = roleService;
        this.noteService = noteService;
        this.notesShare = true;
        this.responseHidden = true;
    }
    NotesComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.selectedNote = new file_1.MyFile();
        this.noteService.get_notes().subscribe(function (json) {
            console.log(json);
            _this.notes = json;
        }, function (error) { return console.error('Error: ' + error); });
    };
    NotesComponent.prototype.onSelectNote = function (note) {
        this.selectedNote = note;
    };
    NotesComponent.prototype.isValid = function () {
        return this.selectedNote.created != null;
    };
    NotesComponent.prototype.update_note = function () {
        var _this = this;
        this.noteService.update_note(this.selectedNote).subscribe(function (json) {
            console.log(json);
            _this.showResponse("Note updated successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.showResponse("Note update failed");
        });
    };
    NotesComponent.prototype.delete_note = function () {
        var _this = this;
        this.noteService.delete_note(this.selectedNote.id).subscribe(function (json) {
            console.log(json);
            _this.notes.splice(_this.notes.indexOf(_this.selectedNote), 1);
            _this.selectedNote = new file_1.MyFile();
            _this.showResponse("Note deleted successfully");
        }, function (error) {
            console.error('Error: ' + error);
            _this.showResponse("Note delete failed");
        });
    };
    NotesComponent.prototype.new_note = function () {
        var _this = this;
        if (this.isValid()) {
            this.selectedNote = new file_1.MyFile();
        }
        else {
            this.noteService.new_note(this.selectedNote).subscribe(function (json) {
                console.log(json);
                _this.notes.push(json);
                _this.showResponse("Note created successfully");
                _this.selectedNote = new file_1.MyFile();
            }, function (error) {
                console.error('Error: ' + error);
                _this.showResponse("Note creation failed");
            });
        }
    };
    NotesComponent.prototype.showShare = function () {
        this.notesShare = false;
    };
    NotesComponent.prototype.showResponse = function (event) {
        var _this = this;
        this.requestResponse = event;
        this.responseHidden = false;
        setTimeout(function () { return _this.responseHidden = true; }, 1500);
    };
    NotesComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            selector: 'notes',
            templateUrl: './notes.component.html',
            styleUrls: ['./notes.component.css']
        }),
        __metadata("design:paramtypes", [file_service_1.FileService,
            role_service_1.RoleService,
            note_service_1.NoteService])
    ], NotesComponent);
    return NotesComponent;
}());
exports.NotesComponent = NotesComponent;
//# sourceMappingURL=notes.component.js.map