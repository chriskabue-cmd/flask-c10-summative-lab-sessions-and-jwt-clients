from flask import Flask, request, session
from models import db, User, Note, bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'secret'

# Enable CORS for session-based auth
CORS(app, supports_credentials=True)

db.init_app(app)
bcrypt.init_app(app)


# -------- AUTH --------

@app.post("/signup")
def signup():
    data = request.get_json()

    # prevent duplicate usernames
    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return {"error": "Username already exists"}, 400

    user = User(username=data["username"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return {"message": "User created"}, 201


@app.post("/login")
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        session["user_id"] = user.id
        return {"message": "Logged in"}

    return {"error": "Invalid credentials"}, 401


@app.delete("/logout")
def logout():
    session.pop("user_id", None)
    return {"message": "Logged out"}


@app.get("/me")
def me():
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Unauthorized"}, 401

    user = User.query.get(user_id)

    return {
        "id": user.id,
        "username": user.username
    }


# -------- HELPER --------

def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


# -------- NOTES (CRUD) --------

@app.get("/check_session")
def check_session():
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Unauthorized"}, 401

    user = User.query.get(user_id)

    return {
        "id": user.id,
        "username": user.username
    }

@app.post("/notes")
def create_note():
    user = current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()

    note = Note(
        title=data["title"],
        content=data["content"],
        user_id=user.id
    )

    db.session.add(note)
    db.session.commit()

    return {"message": "Created"}, 201


@app.patch("/notes/<int:id>")
def update_note(id):
    user = current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    note = Note.query.get(id)

    if not note or note.user_id != user.id:
        return {"error": "Not found"}, 404

    data = request.get_json()

    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)

    db.session.commit()

    return {"message": "Updated"}


@app.delete("/notes/<int:id>")
def delete_note(id):
    user = current_user()
    if not user:
        return {"error": "Unauthorized"}, 401

    note = Note.query.get(id)

    if not note or note.user_id != user.id:
        return {"error": "Not found"}, 404

    db.session.delete(note)
    db.session.commit()

    return {"message": "Deleted"}


# -------- RUN --------

if __name__ == "__main__":
    app.run(debug=True)