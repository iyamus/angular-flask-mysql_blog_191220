from flask import Flask, request, jsonify
import json
from flask_mysqldb import MySQL
import pyrebase

#import flask_mysqlDB
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename


# local uploads or temp
UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


# filter mime-types
def allowed_files(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)

# config
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "db_blog"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
mysql = MySQL(app)
CORS(app)

# firebase config
config = {
    
}
# serviceAccount는 해당 폴더에 firebase가 접근 및 수정하기 위해 필요.


# init firebase app
firebase = pyrebase.initialize_app(config)
# firebase storage
storage = firebase.storage()


@app.route("/api/posts", methods=["GET"])
def index():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute(""" SELECT * FROM flaskposts """)

        posts = cur.fetchall()
        return jsonify(data=posts)


@app.route("/api/addpost", methods=["POST"])
def addpost():
    if request.method == "POST":
        print(request.form, flush=True)
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["photo"]

        if photo and allowed_files(photo.filename):
            filename = str(uuid.uuid4())
            filename += "."
            filename += photo.filename.split(".")[1]
            # create secure name
            filename_secure = secure_filename(filename)
            # save the file inside the uploads folder
            photo.save(os.path.join(
                app.config["UPLOAD_FOLDER"], filename_secure))
            # local file
            local_filename = "./uploads/"
            local_filename += filename_secure
            # firebase filename
            firebase_filename = "uploads/"
            firebase_filename += filename_secure
            # upload the file
            storage.child(firebase_filename).put(local_filename)
            # get the url of the file
            photo_image = storage.child(firebase_filename).get_url(None)
            # get cursor to exec the mysql functions
            print("check: "+title+"/" + content+"/" +
                  photo_image+"/" + filename_secure)
            cur = mysql.connection.cursor()
            # cur.execute("""INSERT INTO flaskposts (title, content, photo, photoname) VALUES (%s, %s, %s, %s) """,
            #     (title, content, photo_image, filename_secure)
            # )
            cur.execute("INSERT INTO flaskposts (title, content, photo, photoname) VALUES ('" +
                        title+"','"+content+"','"+photo_image+"','"+filename_secure+"' )")
            mysql.connection.commit()
            os.remove(os.path.join(
                app.config["UPLOAD_FOLDER"], filename_secure))
            return jsonify(data="The post was created successfully")


@app.route("/api/post/<id>", methods=["GET"])
def singlepost(id):
    cur = mysql.connection.cursor()
    cur.execute(" SELECT * FROM flaskposts WHERE id = '" + id + "' ")
    record = cur.fetchone()
    return jsonify(data=record)


@app.route("/api/editfullpost/<id>", methods=["PUT"])
def editfullpost(id):
    if request.method == "PUT":
        print(request.form, flush=True)
        postid = request.form.get("id")
        title = request.form.get("title")
        content = request.form.get("content")
        oldphoto = request.form.get("oldphoto")
        photoname = request.form.get("photoname")

        if request.files["photo"]:
            if allowed_files(request.files["photo"].filename):
                photo = request.files["photo"]
                # creating the filename
                filename = str(uuid.uuid4())
                filename += "."
                filename += photo.filename.split(".")[1]
                # create a secure name
                filename_secure = secure_filename(filename)
                # save the file inside the folder specified
                photo.save(os.path.join(
                    app.config["UPLOAD_FOLDER"], filename_secure))
                # local file
                local_filename = "./uploads/"
                local_filename += filename_secure
                # firebase file name
                firebase_filename = "uploads/"
                firebase_filename += filename_secure
                # upload the file
                storage.child(firebase_filename).put(local_filename)
                # get the url
                photo_image = storage.child(firebase_filename).get_url(None)
                # get the cursor to exec the mysql functions
                cur = mysql.connection.cursor()
                # update the values
                cur.execute(""" UPDATE flaskposts SET title=%s, content=%s, photo=%s, photoname=%s WHERE id=%s """,
                            (title, content, photo_image, filename_secure, postid))
                mysql.connection.commit()
                # delete the current image
                os.remove(os.path.join(
                    app.config["UPLOAD_FOLDER"], filename_secure))
                # path of the image to delete inside firebase
                firebase_filename_delete = "uploads/"
                firebase_filename_delete += photoname
                storage.delete(firebase_filename_delete)
                return jsonify(data="the post was updated successfully")


@app.route("/api/editpost/<id>", methods=["PUT"])
def editpost(id):
    if request.method == "PUT":
        postid = request.form.get("id")
        title = request.form.get("title")
        content = request.form.get("content")
        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE flaskposts SET title=%s, content=%s WHERE id=%s  """,
                    (title, content, postid))
        mysql.connection.commit()
    return jsonify(data="The post was updated successfully")


@app.route("/api/deletepost/<id>", methods=["DELETE"])
def deletepost(id):
    postid = request.form["id"]
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM flaskposts WHERE id=%s  """ % (postid))
    mysql.connection.commit()
    return jsonify(data="post was deleted successfully")


if __name__ == "__main__":
    app.run(debug=True)
