from app import db
from datetime import datetime
import json

class SampleResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.String(64), unique=True, nullable=False)
    image_path = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    counts_json = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "sample_id": self.sample_id,
            "image_path": self.image_path,
            "timestamp": self.timestamp.isoformat(),
            "counts": json.loads(self.counts_json or "{}")
        }
