import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { HttpModule }    from '@angular/http';
import { FormsModule }   from '@angular/forms';

import { AppComponent }  from './app.component';
import { LoginComponent }  from './login/login.component';
import { UserService} from './services/user.service';
import { FileService} from './services/file.service';
import { RegisterComponent }  from './register/register.component';
import { UploadComponent }  from './upload/upload.component';
import { ActivateComponent }  from './activate/activate.component';
import { NotFoundComponent }  from './notfound/not-found.component';
import { ResetComponent }  from './reset/reset.component';
import { FilesComponent } from './files/files.component';
import { SettingsComponent } from './settings/settings.component';

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
                  SettingsComponent],
  bootstrap:    [ AppComponent ],
  providers: [ UserService,
                FileService ],
})
export class AppModule { }
