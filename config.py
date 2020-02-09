from flask import Flask
import pyodbc
from flask_sqlalchemy import SQLAlchemy        

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://tabnav:WU4MY2Ea@10.100.150.49/Assessment?driver=SQL+server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'HeyYo!' 
