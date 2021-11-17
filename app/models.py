from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#quote model 
class Quotes: 
  '''Class to display random quotes'''
  def __init__(self,author,quote):
    self.author = author
    self.quote = quote
# db model
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    
    @property
    def password(self):
      raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self, password):
      self.pass_secure = generate_password_hash(password)
    def verify_password(self,password):
      return check_password_hash(self.pass_secure,password)  

    def __repr__(self):
        return f'User {self.username}'  
class BlogPost(db.Model):
    __tablename__ = 'blog'
    id =db.Column(db.Integer, primary_key=True)  
    title =db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='unknown' )
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    
    def __repr__(self):
      return 'Blog post' + str(self.id) 