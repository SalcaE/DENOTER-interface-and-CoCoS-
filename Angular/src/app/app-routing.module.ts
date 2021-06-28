import { NgModule } from '@angular/core';

import { RouterModule, Routes } from '@angular/router';
import { CreateComponent } from './create/create.component';
import {DENOTERComponent} from './DENOTER/DENOTER.component';

const routes: Routes = [
  { path: 'create', component: CreateComponent },
  { path: '', component: DENOTERComponent, pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
