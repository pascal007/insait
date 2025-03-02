from models.GeneratedText import GeneratedText
from models.User import User
from resources.extensions import db


def test_create_user(test_app):
    with test_app.app_context():
        user = User(username="user", password_hash="password")
        db.session.add(user)
        db.session.commit()
        assert bool(User.query.filter_by(username="user").first()) is not False


def test_create_generated_text(test_app):
    with test_app.app_context():
        user = User(username="user", password_hash="password")
        db.session.add(user)
        db.session.commit()

        generated_text = GeneratedText(
            user_id=user.id, prompt="Test prompt", response="Generated response"
        )
        db.session.add(generated_text)
        db.session.commit()

        assert GeneratedText.query.filter_by(user_id=user.id).first() is not None
