from flask_login import UserMixin
from app import db  # Import db after app is initialized
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # Hashed password
    role = db.Column(db.String(10), nullable=False, default='user')  # 'user' or 'admin'

    # Relationship to Measurements (one-to-many)
    measurements = db.relationship('Measurement', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.email}', Role: '{self.role}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @property
    def is_admin(self):
        return self.role == 'admin'

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chest = db.Column(db.Float, nullable=False)
    waist = db.Column(db.Float, nullable=False)
    inseam = db.Column(db.Float, nullable=False)
    head = db.Column(db.Float, nullable=False)
    neck_circumference = db.Column(db.Float, nullable=False)
    shoulder_width = db.Column(db.Float, nullable=False)
    sleeve_length = db.Column(db.Float, nullable=False)
    buba_length = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Foreign key to link measurement to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Measurement(User ID: {self.user_id}, Chest: {self.chest}, Waist: {self.waist}, Inseam: {self.inseam})"
