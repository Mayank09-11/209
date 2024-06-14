from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
from models import User, Music
from database import engine, Base, get_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Create the database tables
Base.metadata.create_all(bind=engine)

@app.post("/register")
def register():
    db = next(get_db())
    username = request.json["username"]
    password = request.json["password"]
    hashed_password = generate_password_hash(password)
    
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return jsonify({"message": "User created successfully!"})

@app.post("/login")
def login():
    db = next(get_db())
    username = request.json["username"]
    password = request.json["password"]
    
    user = db.query(User).filter(User.username == username).first()
    if user and check_password_hash(user.hashed_password, password):
        return jsonify({"message": "Login successful!"})
    return jsonify({"message": "Invalid credentials"}), 401

@app.post("/upload")
def upload():
    db = next(get_db())
    title = request.json["title"]
    artist = request.json["artist"]
    filename = request.json["filename"]
    owner_id = request.json["owner_id"]
    
    music = Music(title=title, artist=artist, filename=filename, owner_id=owner_id)
    db.add(music)
    db.commit()
    db.refresh(music)
    return jsonify({"message": "Music uploaded successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
