from werkzeug.security import generate_password_hash, check_password_hash
from . import db, ma
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Phone = db.Column(db.String(100))
    Email =db.Column(db.String(100), unique=True)
    Position = db.Column(db.String(100))
    Department = db.Column(db.String(100))
    Password = db.Column(db.String(128))
    Status = db.Column(db.String(100))
    Role = db.Column(db.String(100))

    def set_password(self, user_password):
        self.Password = generate_password_hash(user_password)

    def check_password(self, user_password):
        return check_password_hash(self.PasswordHash, user_password)


class Session(db.Model):
   __tablename__ = 'sessions'

   SessionID = db.Column(db.Integer, primary_key=True)
   UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
   Name = db.Column(db.String(100))
#    Email = db.Column(db.String(100))
   IPAddress = db.Column(db.String(39))
   Timestamp =  db.Column(db.DateTime, default=datetime.utcnow)
   

   # define the relationship with User entity
   User = db.relationship('User', foreign_keys=[UserID])

   def __repr__(self):
        return f"<Session {self.SessionID}>"

   # Product Schema
class  UserSchema(ma.Schema):
    class Meta:
        fields = ('UserID', 'Name', 'Phone', 'Email', 'Position','Department', 'Role' )

# Init Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class  SessionsSchema(ma.Schema):
    class Meta:
        fields = ('SessionID','UserID', 'Name', 'Timestamp')

# Init Schema
session_schema = SessionsSchema()
sessions_schema = SessionsSchema(many=True)