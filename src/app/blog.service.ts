import { Injectable } from "@angular/core";

import { HttpClient } from "@angular/common/http";
import { Post } from "./post";
import { Observable, of } from "rxjs";

@Injectable({
  providedIn: "root"
})
export class BlogService {
  constructor(private httpClient: HttpClient) {}

  public server: string = "http://localhost:5000/api/";

  public getPosts() {
    return this.httpClient.get<Post>(this.server + "posts");
  }

  public getPost(postId: string) {
    return this.httpClient.get<Post>(this.server + `post/${postId}`);
  }

  public addPost(postObj: Post, image: any) {
    console.log(image);

    const { title, content } = postObj;
    const formData: FormData = new FormData();

    formData.append("title", title);
    formData.append("content", content);
    formData.append("photo", image[0], image["filename"]);
    return this.httpClient.post<Post>(this.server + "addpost", formData);
  }

  public editPost(postObj: Post, image: any) {
    const { title, content, id, oldphoto, photoname } = postObj;
    const formData: FormData = new FormData();

    formData.append("id", id);
    formData.append("title", title);
    formData.append("content", content);
    formData.append("oldphoto", oldphoto);
    formData.append("photoname", photoname);
    if (image !== undefined) {
      formData.append("photo", image[0], image["filename"]);
      return this.httpClient.put<Post>(
        this.server + `editfullpost/${id}`,
        formData
      );
    } else {
      return this.httpClient.put<Post>(
        this.server + `editpost/${id}`,
        formData
      );
    }
  }

  public deletePost(postId: number) {
    const formData: FormData = new FormData();
    formData.append("id", postId);

    return this.httpClient.request(
      "delete",
      this.server + `deletepost/${postId}`,
      { body: formData }
    );
  }
}
