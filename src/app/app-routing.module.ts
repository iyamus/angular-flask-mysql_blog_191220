import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MainComponent } from './main/main.component';
import { AddpostComponent } from './addpost/addpost.component';
import { PostComponent } from './post/post.component';


const routes: Routes = [
  { path: "", redirectTo: "/posts", pathMatch: "full" },
  { path: "posts", component: MainComponent },
  { path: "addpost", component: AddpostComponent },
  { path: "post/:id", component: PostComponent }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
