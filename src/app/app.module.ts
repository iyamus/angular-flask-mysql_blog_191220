import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { MainComponent } from "./main/main.component";
import { AddpostComponent } from "./addpost/addpost.component";
import { PostComponent } from "./post/post.component";

import { HttpClientModule } from "@angular/common/http";
import { FormsModule } from "@angular/forms";
import { ReactiveFormsModule } from "@angular/forms";
import { APP_BASE_HREF } from '@angular/common';

@NgModule({
  declarations: [AppComponent, MainComponent, AddpostComponent, PostComponent],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [{provide: APP_BASE_HREF, useValue: '/'}],
  bootstrap: [AppComponent]
})
export class AppModule {}
