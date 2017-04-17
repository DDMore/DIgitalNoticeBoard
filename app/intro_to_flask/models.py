from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash,check_password_hash
db=SQLAlchemy()
    
class User(db.Model):
  __tablename__ = 'register'
  
  username = db.Column(db.String(100),primary_key=True)
  
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(54))
   
  def __init__(self, username,email,password):
    self.username = username.title()
    #self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.password = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.password, password)
	
