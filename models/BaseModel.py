import uuid
from datetime import datetime

from resources.extensions import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
