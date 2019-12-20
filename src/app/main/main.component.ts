import { Component, OnInit } from "@angular/core";
import { BlogService } from "../blog.service";
import { Subscription } from "rxjs";

@Component({
  selector: "app-main",
  templateUrl: "./main.component.html",
  styleUrls: ["./main.component.css"]
})
export class MainComponent implements OnInit {
  constructor(private flaskApiService: BlogService) {}
  public posts: any[];
  public postsSubscription: Subscription;

  public getPosts() {
    this.postsSubscription = this.flaskApiService.getPosts().subscribe(p => {
      this.posts = p["data"];
      console.log(this.posts);
    });
  }

  ngOnInit() {
    this.getPosts();
  }

  ngOnDestroy() {
    this.postsSubscription.unsubscribe();
  }
}
