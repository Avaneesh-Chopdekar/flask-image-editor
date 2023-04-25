import os
import cv2
from flask import Flask, flash, request, render_template
from werkzeug.utils import secure_filename
from env_variables import *


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def process_img(filename, operation):
    print(f"{filename} will be {operation}")

    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            img_processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_filename = f"static/{filename}"
            cv2.imwrite(new_filename, img_processed)
            return new_filename
        case "cwebp":
            new_filename = f"static/{filename.rsplit('.', 1)[0]}.webp"
            cv2.imwrite(new_filename, img)
            return new_filename
        case "cpng":
            new_filename = f"static/{filename.rsplit('.', 1)[0]}.png"
            cv2.imwrite(new_filename, img)
            return new_filename
        case "cjpg":
            new_filename = f"static/{filename.rsplit('.', 1)[0]}.jpg"
            cv2.imwrite(new_filename, img)
            return new_filename


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return "error"
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            new_img = process_img(filename, operation)
            flash(
                f"Your image has been processed successfully! <a href='/{new_img}' download target='_blank'>save here</a>"
            )
            return render_template("index.html")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
