from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    concerns = db.relationship('Concern', backref='user', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

class Concern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    votes = db.relationship('Vote', backref='concern', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='concern', lazy=True, cascade='all, delete-orphan')
    
    @property
    def upvotes(self):
        return Vote.query.filter_by(concern_id=self.id, vote_type='up').count()
    
    @property
    def downvotes(self):
        return Vote.query.filter_by(concern_id=self.id, vote_type='down').count()

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    concern_id = db.Column(db.Integer, db.ForeignKey('concern.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)  # 'up' or 'down'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure one vote per user per concern
    __table_args__ = (db.UniqueConstraint('user_id', 'concern_id', name='unique_user_concern_vote'),)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    concern_id = db.Column(db.Integer, db.ForeignKey('concern.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)