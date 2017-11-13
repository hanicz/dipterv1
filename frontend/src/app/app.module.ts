import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { HttpModule }    from '@angular/http';
import { FormsModule }   from '@angular/forms';

import { AppComponent }  from './app.component';
import { LoginComponent }  from './login/login.component';
import { UserService} from './services/user.service';
import { FileService} from './services/file.service';
import { LogService} from './services/log.service';
import { RoleService} from './services/role.service';
import { NoteService} from './services/note.service';
import { ShareService} from './services/share.service';
import { DropboxService} from './services/dropbox.service';
import { RegisterComponent }  from './register/register.component';
import { UploadComponent }  from './upload/upload.component';
import { ActivateComponent }  from './activate/activate.component';
import { NotFoundComponent }  from './notfound/not-found.component';
import { ResetComponent }  from './reset/reset.component';
import { FilesComponent } from './files/files.component';
import { SettingsComponent } from './settings/settings.component';
import { LogsComponent } from './logs/logs.component';
import { FileDetailComponent } from './file-detail/file-detail.component';
import { FolderDetailComponent } from './folder-detail/folder-detail.component';
import { DeletedFilesComponent } from './deleted-files/deleted-files.component';
import { ShareComponent } from './share/share.component';
import { NotesComponent } from './notes/notes.component';
import { CreateFolderComponent } from './create-folder/create-folder.component';
import { DropboxComponent } from './dropbox/dropbox.component';
import { SharedWithMeComponent } from './shared-with-me/shared-with-me.component'
import { SharedNotesComponent } from './shared-notes/shared-notes.component';
import { ResponseComponent } from './reponse/response.component';
import { DropboxDownloadComponent } from './dropbox-download/dropbox-download.component';
import {  TruncatePipe }   from './entities/pipe';

@NgModule({
  imports:      [ BrowserModule,
                  AppRoutingModule,
                  HttpModule,
                  FormsModule ],
  declarations: [ AppComponent,
                  LoginComponent,
                  RegisterComponent,
                  ActivateComponent,
                  NotFoundComponent,
                  ResetComponent,
                  UploadComponent,
                  FilesComponent,
                  SettingsComponent,
                  LogsComponent,
                  FileDetailComponent,
                  FolderDetailComponent,
                  DeletedFilesComponent,
                  ShareComponent,
                  NotesComponent,
                  CreateFolderComponent,
                  DropboxComponent,
                  SharedWithMeComponent,
                  SharedNotesComponent,
                  TruncatePipe,
                  ResponseComponent,
                  DropboxDownloadComponent],
  bootstrap:    [ AppComponent ],
  providers: [ UserService,
                FileService,
                LogService,
                RoleService,
                ShareService,
                NoteService,
                DropboxService ],
})
export class AppModule { }
