from models.BaseModel import BaseModel
from resources.extensions import db


class GeneratedText(BaseModel):
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': str(self.id),
            'prompt': self.prompt,
            'response': self.response
        }
