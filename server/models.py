from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates ("name")
    def validate_name(self, key, _name):
        if _name == "":
            raise ValueError("Name is a must")
        existing_author = Author.query.filter_by(name=_name).first()
        if existing_author:
            raise ValueError("Name must be unique")
        return _name
    
    @validates("phone_number")
    def validate_phone(self, key, _phone_number):
        if not isinstance(_phone_number, str) or len(_phone_number) != 10 or not _phone_number.isdigit():
            raise ValueError("Phone number digits must equal 10")
        return _phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates ("title")
    def validate_title (self, key, _title):
        if not any(keyword in _title for keyword in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError("Title not clickbaity enough")
        return _title
    
    @validates("category")
    def validate_category(self, key, _category):
        ava_categories = ["Fiction", "Non-Fiction"]
        if _category not in ava_categories:
            raise ValueError("Not a valid genre")
        return _category
    
    @validates("content")
    def validate_content(self, key, _content):
        if not len(_content) >= 250:
            raise ValueError("Content too short")
        return _content
    
    @validates("summary")
    def validate_summary(self, key, _summary):
        if not len(_summary) <= 250:
            raise ValueError("Summary too long")
        return _summary

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
