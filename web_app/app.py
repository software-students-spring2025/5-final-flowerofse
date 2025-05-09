from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime
import os
import zipfile
import uuid
from werkzeug.utils import secure_filename
from flask import send_from_directory

mongo = PyMongo()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.secret_key = "dev"
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/gameforum")
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")    

    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    register_routes(app)

    return app


class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc["_id"])
        self.username = user_doc["username"]


def register_routes(app):
    @app.route("/")
    def home():
        games = list(mongo.db.games.find())
        return render_template("home.html", games=games)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        error = None
        if request.method == "POST":
            username = request.form["username"]
            password = generate_password_hash(request.form["password"], method='pbkdf2:sha256')
            if mongo.db.users.find_one({"username": username}):
                error = "Username already exists"
            else:
                mongo.db.users.insert_one({"username": username, "password": password})
                return redirect(url_for("login"))
        return render_template("register.html", error=error)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user_doc = mongo.db.users.find_one({"username": username})
            if user_doc and check_password_hash(user_doc["password"], password):
                login_user(User(user_doc))
                return redirect(url_for("home"))
            else:
                error = "Invalid username or password"
        return render_template("login.html", error=error)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("home"))

    @app.route("/upload", methods=["GET", "POST"])
    @login_required
    def upload_game():
        if request.method == "POST":
            file = request.files["game_file"]
            cover_file = request.files.get("cover_image")
            if not file.filename.endswith(".zip"):
                return "Only ZIP files are allowed."

            game_id = str(uuid.uuid4())
            folder_path = os.path.join(app.config["UPLOAD_FOLDER"], game_id)
            os.makedirs(folder_path)

            zip_path = os.path.join(folder_path, secure_filename(file.filename))
            file.save(zip_path)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(folder_path)

            if cover_file and cover_file.filename.lower().endswith(".png"):
                cover_path = os.path.join(folder_path, "cover.png")
                cover_file.save(cover_path)
            else:
                default_cover = os.path.join(app.root_path, "static", "default_cover.png")
                cover_path = os.path.join(folder_path, "cover.png")
                if os.path.exists(default_cover):
                    from shutil import copyfile
                    copyfile(default_cover, cover_path)
                else:
                    print("default_cover.png not found")


            mongo.db.games.insert_one({
                "title": request.form["title"],
                "description": request.form["description"],
                "folder": game_id,
                "cover_image": f"{game_id}/cover.png",
                "author_id": ObjectId(current_user.id),
                "created_at": datetime.utcnow()
            })

            return redirect(url_for("home"))
        return render_template("upload.html")

    @app.route("/game/<game_id>")
    def game_detail(game_id):
        game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
        comments = list(mongo.db.comments.aggregate([
            {"$match": {"game_id": game_id}},
            {"$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }},
            {"$unwind": {"path": "$user", "preserveNullAndEmptyArrays": True}}
        ]))
        return render_template("game_detail.html", game=game, comments=comments)

    @app.route("/comment/<game_id>", methods=["POST"])
    @login_required
    def comment(game_id):
        mongo.db.comments.insert_one({
            "game_id": game_id,
            "user_id": ObjectId(current_user.id),
            "content": request.form["comment"],
            "timestamp": datetime.utcnow()
        })
        return redirect(url_for("game_detail", game_id=game_id))
    
    @app.route('/games/<path:filename>')
    def serve_game(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@login_manager.user_loader
def load_user(user_id):
    user_doc = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_doc) if user_doc else None


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000)