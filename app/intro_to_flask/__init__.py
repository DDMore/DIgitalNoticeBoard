from flask import Flask
 
app = Flask(__name__)
 
app.secret_key = 'development key'
 

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:dmm@localhost/noticeboard'
#from routes import mail
#mail.init_app(app)
 
import intro_to_flask.routes 

from models import db
db.init_app(app)

 




