import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { HttpModule }    from '@angular/http';
import { FormsModule }   from '@angular/forms';

import { AppComponent }  from './app.component';
import { LoginComponent }  from './login/login.component';
import { UserService} from './services/user.service';
import { RegisterComponent }  from './register/register.component';
import { ActivateComponent }  from './activate/activate.component';
import { NotFoundComponent }  from './notfound/not-found.component';

@NgModule({
  imports:      [ BrowserModule,
                  AppRoutingModule,
                  HttpModule,
                  FormsModule ],
  declarations: [ AppComponent,
                  LoginComponent,
                  RegisterComponent,
                  ActivateComponent,
                  NotFoundComponent],
  bootstrap:    [ AppComponent ],
  providers: [ UserService ],
})
export class AppModule { }
