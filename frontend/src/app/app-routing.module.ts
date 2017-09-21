/**
 * Created by Hanicz on 2/19/2017.
 */
import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent }  from './login/login.component';
import { RegisterComponent }  from './register/register.component';
import { ActivateComponent }  from './activate/activate.component';
import { ResetComponent }  from './reset/reset.component';
import { NotFoundComponent }  from './notfound/not-found.component';
import { UploadComponent }  from './upload/upload.component';
import { FilesComponent }  from './files/files.component';
import { SettingsComponent }  from './settings/settings.component';
import { LogsComponent }  from './logs/logs.component';
import { DeletedFilesComponent }  from './deleted-files/deleted-files.component';


const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login',  component: LoginComponent },
  { path: 'register',  component: RegisterComponent },
  { path: 'reset/:token',  component: ResetComponent },
  { path: 'activate/:token', component: ActivateComponent },
  { path: 'not-found', component: NotFoundComponent },
  { path: 'upload', component: UploadComponent },
  { path: 'files', component: FilesComponent },
  { path: 'settings', component: SettingsComponent },
  { path: 'logs', component: LogsComponent },
  { path: 'deleted-files', component: DeletedFilesComponent },
  { path: '**', redirectTo: '/not-found' }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
