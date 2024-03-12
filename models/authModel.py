from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from . import db, ma


class User(db.Model):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Phone = db.Column(db.String(100))
    Email =db.Column(db.String(100), unique=True)
    Position = db.Column(db.String(100))
    Department = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    Status = db.Column(db.String(100))
    Role = db.Column(db.String(100))


class Session(db.Model):
   __tablename__ = 'sessions'

   SessionID = db.Column(db.Integer, primary_key=True)
   UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
   Name = db.Column(db.String(100))
   Phone = db.Column(db.String(100))
   Email = db.Column(db.String(100), unique=True)
   Position = db.Column(db.String(100))
   Department = db.Column(db.String(100))
   Password = db.Column(db.String(100))
   Status = db.Column(db.String(100))
   Role = db.Column(db.String(100))


   # define the relationship with User entity
   User = db.relationship('User', foreign_keys=[UserID])


   # Product Schema
class  UserSchema(ma.Schema):
    class Meta:
        fields = ('UserID', 'Name', 'Phone', 'Email', 'Position','Department', 'Role' )

# Init Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class  SessionsSchema(ma.Schema):
    class Meta:
        fields = ('SessionID','UserID', 'Name', 'Phone', 'Email', 'Position','Department', 'Role' )

# Init Schema
session_schema = SessionsSchema()
sessions_schema = SessionsSchema(many=True)
