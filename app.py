# This is the root app for the Assessment office. 
from flask import redirect, render_template, request, session, flash
from config import app, db
from models import Caregiver, Concern, MTSSchecks, MTSScomment, Intervention, SSTmember, Student, Treatment 
import routes

###############################################
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'Sorry! No response. Try again.'

if __name__=="__main__":    
    app.run(debug=True)     