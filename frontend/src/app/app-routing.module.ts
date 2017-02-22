/**
 * Created by Hanicz on 2/19/2017.
 */
import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent }  from './login/login.component';
import { RegisterComponent }  from './register/register.component';
import { ActivateComponent }  from './activate/activate.component';
import { NotFoundComponent }  from './notfound/not-found.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login',  component: LoginComponent },
  { path: 'register',  component: RegisterComponent },
  { path: 'activate/:token', component: ActivateComponent },
  { path: 'not-found', component: NotFoundComponent },
  {path: '**', redirectTo: '/not-found'}
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
