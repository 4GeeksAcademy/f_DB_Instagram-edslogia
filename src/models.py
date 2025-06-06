from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum, Date, Time, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from eralchemy2 import render_er
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    country: Mapped[str] = mapped_column()
    gender: Mapped[str] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "gender": self.gender,
            "country": self.country
        }

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }

class Post(db.Model):    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    date_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    def serialize(self):
        return{
            "user_id": self.user_id,
            "date_time": self.date_time
        }
    
class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(180))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    date: Mapped[datetime.date] = mapped_column(Date(), nullable=False)
    time: Mapped[datetime.time] = mapped_column(Time(), nullable=False)

    def serialize(self):
        return {
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
            "date": self.date,
            "time": self.time
        }
    
class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum('image', 'video', name='media_type'), nullable=False)
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    def serialize(self):
        return{ 
            "type" : self.type,
            "url" : self.url,
            "post_id" : self.post_id
        }

try:
    render_er(db.Model, 'diagram.png')
    print("✅ Diagrama generado correctamente como diagram.png")
except Exception as e:
    print("❌ Error generando el diagrama:", e)