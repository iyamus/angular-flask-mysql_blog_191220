import { Component, OnInit } from "@angular/core";
import { Post } from "../post";
import {
  FormsModule,
  FormControl,
  Validators,
  FormGroup
} from "@angular/forms";
import { Router } from "@angular/router";
import { BlogService } from "../blog.service";

@Component({
  selector: "app-addpost",
  templateUrl: "./addpost.component.html",
  styleUrls: ["./addpost.component.css"]
})
export class AddpostComponent implements OnInit {
  constructor(private blogService: BlogService, private router: Router) {}

  public image: any = null;
  public busy: boolean;

  public postForm = new FormGroup({
    title: new FormControl("", Validators.required),
    content: new FormControl("", Validators.required),
    photo: new FormControl("", Validators.required)
  });

  public handleInput($event: Event) {
    this.image = $event.target["files"];
    console.log(this.image);
  }

  public addPost(post: Post) {
    this.busy = true;
    this.blogService.addPost(post, this.image).subscribe(res => {
      this.busy = false;
      console.log(res);
      this.router.navigate(["/"]);
    });
  }
  ngOnInit() {}
}
