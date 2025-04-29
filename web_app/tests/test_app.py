import os
import pytest
import tempfile
import zipfile
from web_app.app import create_app, mongo
from werkzeug.security import generate_password_hash
from bson import ObjectId

@pytest.fixture
def app():
    # Check if we're running inside Docker (common CI/CD setups set HOSTNAME inside container)
    is_inside_docker = os.path.exists("/.dockerenv") or os.getenv("CI") == "true"

    if is_inside_docker:
        mongo_uri = "mongodb://mongodb:27017/test_gameforum"
    else:
        mongo_uri = "mongodb://127.0.0.1:27017/test_gameforum"

    os.environ["MONGO_URI"] = mongo_uri

    test_app = create_app()
    test_app.config["TESTING"] = True
    test_app.config["UPLOAD_FOLDER"] = tempfile.mkdtemp()
    return test_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        mongo.db.users.delete_many({})
        mongo.db.games.delete_many({})
        mongo.db.comments.delete_many({})
        yield
        mongo.db.users.delete_many({})
        mongo.db.games.delete_many({})
        mongo.db.comments.delete_many({})

def test_home(client):
    rv = client.get("/")
    assert rv.status_code == 200

def test_register_and_login(client):
    rv = client.post("/register", data={"username": "newuser", "password": "newpass"}, follow_redirects=True)
    assert rv.status_code == 200
    assert mongo.db.users.find_one({"username": "newuser"}) is not None

    rv = client.post("/login", data={"username": "newuser", "password": "newpass"}, follow_redirects=True)
    assert rv.status_code == 200

def test_login_fail(client):
    rv = client.post("/login", data={"username": "nouser", "password": "wrong"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Invalid username or password" in rv.data

def test_upload_game(client):
    game_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    with zipfile.ZipFile(game_zip, "w") as zipf:
        zipf.writestr("dummy.txt", "test")
    game_zip.seek(0)

    user_id = mongo.db.users.insert_one({
        "username": "testuser",
        "password": generate_password_hash("testpass")
    }).inserted_id
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user_id)

    data = {
        "title": "Test Game",
        "description": "desc",
        "game_file": (open(game_zip.name, "rb"), "game.zip"),
        "cover_image": (tempfile.NamedTemporaryFile(suffix=".png"), "cover.png"),
    }
    rv = client.post("/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert rv.status_code == 200
    assert mongo.db.games.find_one({"title": "Test Game"}) is not None

def test_game_detail(client):
    game_id = mongo.db.games.insert_one({
        "title": "Detail Game",
        "description": "desc",
        "folder": "folder",
        "cover_image": "folder/cover.png",
        "author_id": ObjectId(),
        "created_at": None
    }).inserted_id
    rv = client.get(f"/game/{game_id}")
    assert rv.status_code == 200

def test_comment(client):
    user_id = mongo.db.users.insert_one({
        "username": "commentuser",
        "password": generate_password_hash("commentpass")
    }).inserted_id
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user_id)
    game_id = mongo.db.games.insert_one({
        "title": "Comment Game",
        "description": "desc",
        "folder": "folder",
        "cover_image": "folder/cover.png",
        "author_id": user_id,
        "created_at": None
    }).inserted_id

    rv = client.post(f"/comment/{game_id}", data={"comment": "Nice Game!"}, follow_redirects=True)
    assert rv.status_code == 200
    assert mongo.db.comments.find_one({"content": "Nice Game!"}) is not None

def test_logout(client):
    user_id = mongo.db.users.insert_one({
        "username": "logoutuser",
        "password": generate_password_hash("logoutpass")
    }).inserted_id
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user_id)

    rv = client.get("/logout", follow_redirects=True)
    assert rv.status_code == 200