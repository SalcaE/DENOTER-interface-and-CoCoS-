// @ts-ignore

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {HttpClientModule} from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatButtonModule} from '@angular/material/button';
import {MatToolbarModule} from '@angular/material/toolbar';



import { NavbarComponent } from './navbar/navbar.component';
import { CreateComponent } from './create/create.component';
import {MatIconModule} from '@angular/material/icon';
import { DENOTERComponent } from './DENOTER/DENOTER.component';
import { DndDirective } from './dnd.directive';
import {DragDropModule} from '@angular/cdk/drag-drop';
import {ScrollingModule} from '@angular/cdk/scrolling';
import {MatFormFieldModule} from '@angular/material/form-field';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatOptionModule} from '@angular/material/core';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatInputModule} from '@angular/material/input';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatSelectModule} from '@angular/material/select';

const MaterialComponents = [
  MatButtonModule
];


// @ts-ignore
@NgModule({
  declarations: [
    AppComponent,

    NavbarComponent,
    CreateComponent,
    DENOTERComponent,
    DndDirective,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatProgressBarModule,
    MaterialComponents,
    MatIconModule,
    MatToolbarModule,
    DragDropModule,
    ScrollingModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatOptionModule,
    MatAutocompleteModule,
    MatInputModule,
    FormsModule,
    MatCheckboxModule,
    MatProgressSpinnerModule,
    MatSelectModule
  ],
  exports: [MaterialComponents],
  providers: [],
  bootstrap: [AppComponent],

})
export class AppModule { }
