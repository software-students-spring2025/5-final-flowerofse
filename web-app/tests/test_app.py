import os
import pytest
import tempfile
from app import app, mongo
from flask_login import login_user
from bson import ObjectId
from werkzeug.security import generate_password_hash
import zipfile
@pytest.fixture(autouse=True, scope="function")
def clean_db():
    """Clean up database before and after each test"""
    mongo.db.users.delete_many({})
    mongo.db.games.delete_many({})
    mongo.db.comments.delete_many({})
    yield
    mongo.db.users.delete_many({})
    mongo.db.games.delete_many({})
    mongo.db.comments.delete_many({})

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["UPLOAD_FOLDER"] = tempfile.mkdtemp()
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get("/")
    assert rv.status_code == 200

def test_register_and_login(client):
    # Register
    rv = client.post("/register", data={"username": "newuser", "password": "newpass"}, follow_redirects=True)
    assert rv.status_code == 200
    user = mongo.db.users.find_one({"username": "newuser"})
    assert user is not None

    # Login
    rv = client.post("/login", data={"username": "newuser", "password": "newpass"}, follow_redirects=True)
    assert rv.status_code == 200

def test_login_fail(client):
    rv = client.post("/login", data={"username": "nouser", "password": "wrong"})
    assert b"Invalid credentials" in rv.data

def test_upload_game(client):
    # Create a real small ZIP file for upload
    game_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    with zipfile.ZipFile(game_zip, 'w') as zipf:
        zipf.writestr('dummy.txt', 'this is a test file')

    game_zip.seek(0)
    
    # Create and login user manually
    user_id = mongo.db.users.insert_one({
        "username": "testuser",
        "password": generate_password_hash("testpass")
    }).inserted_id

    with client.session_transaction() as sess:
        sess["_user_id"] = str(user_id)

    data = {
        "title": "Test Game",
        "description": "A test game",
        "game_file": (open(game_zip.name, "rb"), "game.zip"),
        "cover_image": (tempfile.NamedTemporaryFile(suffix=".png"), "cover.png"),
    }
    rv = client.post("/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert rv.status_code == 200
    game = mongo.db.games.find_one({"title": "Test Game"})
    assert game is not None

def test_game_detail(client):
    game_id = mongo.db.games.insert_one({
        "title": "Detail Game",
        "description": "Test desc",
        "folder": "folder",
        "cover_image": "folder/cover.png",
        "author_id": ObjectId(),
        "created_at": None,
    }).inserted_id
    rv = client.get(f"/game/{game_id}")
    assert rv.status_code == 200

def test_comment(client):
    # Create user and login
    user_id = mongo.db.users.insert_one({
        "username": "commentuser",
        "password": generate_password_hash("commentpass")
    }).inserted_id
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user_id)

    # Create game
    game_id = mongo.db.games.insert_one({
        "title": "Comment Game",
        "description": "desc",
        "folder": "folder",
        "cover_image": "folder/cover.png",
        "author_id": user_id,
        "created_at": None,
    }).inserted_id

    rv = client.post(f"/comment/{game_id}", data={"comment": "Nice Game!"}, follow_redirects=True)
    assert rv.status_code == 200
    comment = mongo.db.comments.find_one({"content": "Nice Game!"})
    assert comment is not None

def test_logout(client):
    user_id = mongo.db.users.insert_one({
        "username": "logoutuser",
        "password": generate_password_hash("logoutpass")
    }).inserted_id
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user_id)

    rv = client.get("/logout", follow_redirects=True)
    assert rv.status_code == 200
