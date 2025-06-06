from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum, Date, Time, DateTime, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(16),nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    country: Mapped[str] = mapped_column(String(80))
    gender: Mapped[str] = mapped_column(String(80),nullable=False)
    posts: Mapped[list["Post"]] = relationship("Post", back_populates = "user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "gender": self.gender,
            "country": self.country
        }
    
class Post(db.Model):    
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey('user.id'))
    date_time: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="post")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post_comments")

    def serialize(self):
        return{
            "user_id": self.user_id,
            "date_time": self.date_time
        }

class Follower(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    user_from_id: Mapped[int] = mapped_column(Integer(), ForeignKey('user.id'), nullable=False)
    user_to_id: Mapped[int] = mapped_column(Integer(), ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }

  
class Comment(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(180))
    author_id: Mapped[int] = mapped_column(Integer(), ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(Integer(), ForeignKey('post.id'))
    date: Mapped[datetime.date] = mapped_column(Date(), nullable=False)
    time: Mapped[datetime.time] = mapped_column(Time(), nullable=False)
    post_comments: Mapped["Post"] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
            "date": self.date,
            "time": self.time
        }
    
class Media(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    type: Mapped[str] = mapped_column(Enum('image', 'video', name='media_type'), nullable=False)
    url: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(Integer(), ForeignKey('post.id'))
    size_mb: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)

    def serialize(self):
        return{ 
            "type" : self.type,
            "url" : self.url,
            "post_id" : self.post_id,
            "size_mb" : self.size_mb
        }

try:
    render_er(db.Model, 'diagram.png')
    print("✅ Diagrama generado correctamente como diagram.png")
except Exception as e:
    print("❌ Error generando el diagrama:", e)