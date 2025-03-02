from models.BaseModel import BaseModel
from resources.extensions import db


class User(BaseModel):
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
