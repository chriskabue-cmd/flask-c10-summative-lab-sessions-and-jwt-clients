from app import app
from models import db, User, Note
from flask_cors import CORS

CORS(app, supports_credentials=True)

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(username="test")
    user.set_password("1234")

    db.session.add(user)
    db.session.commit()

    note = Note(title="Sample", content="Hello world", user_id=user.id)
    db.session.add(note)

    db.session.commit()