from flask import render_template, redirect, request, flash, session	# we now need fewer imports because we're not doing everything in this file!
# if we need to work with the database, we'll need those imports:    
from config import db, app
from models import Caregiver, Concern, MTSSchecks, MTSScomment, Intervention, SSTmember, Student, Treatment, Teacher, Outcome
import re
from flask_bcrypt import Bcrypt        
from flask_sqlalchemy import SQLAlchemy        
from sqlalchemy.sql import func
from datetime import datetime, timedelta


bcrypt = Bcrypt(app) 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

def index():
    return render_template('index.html')

def login():
    # validate
    is_valid = True
    if len(request.form['email']) < 1:
        is_valid = False
        flash('Email address is required')
    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        is_valid = False
        flash("Invalid email address!")
    if len(request.form['pw']) < 1:
        is_valid = False
        flash('Password is required')
    if len(request.form['pw']) < 5:
        is_valid = False
        flash('Password must be at least 5 characters')

    # login and store in session
    if is_valid:
        user = SSTmember.query.filter_by(email=request.form['email']).first()
        if user:
            upw = user.pw
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.check_password_hash(upw, request.form['pw']):
                session['userid'] = user.id  
                session['username'] = user.teacher.LASTFIRST
                flash("Welcome {}!".format(user.teacher.FIRST_NAME))                  # if we get True after checking the password, we may put the user id in session
                return redirect('/mtss/dashboard')
        # if we didn't find anything in the database by searching by username or if the passwords don't match,
        # flash an error message and redirect back to a safe route
        flash("You could not be logged in")
        return redirect('/mtss')


def dashboard():
    interventions = Intervention.query.filter_by(status=0).all()
    user = SSTmember.query.filter_by(id=session['userid']).first()
    return render_template('dashboard.html', interventions = interventions, user=user)

def logout():
    session.clear()
    return redirect('/mtss')

def addint():
    interventions = Intervention.query.all()
    user = SSTmember.query.filter_by(id=session['userid']).first()
    treatments = Treatment.query.all()
    concerns = Concern.query.all()
    members = SSTmember.query.all()
    date = datetime.now()
    date = datetime.date(date)
    checkin = date + timedelta(days=14)
    user = SSTmember.query.filter_by(id=session['userid']).first()
    return render_template('addint.html', user=user, interventions=interventions, treatments=treatments, concerns=concerns, members=members, date=date, checkin=checkin)

def createint():
    if request.form['submit'] == "Cancel":
        return redirect ('/mtss/dashboard')
    is_valid = True

    # validate inputs
    if len(request.form['studentid']) < 1:
        is_valid = False
        flash('Student ID number is required.')
    if len(request.form['studentid']) < 5:
        is_valid = False
        flash('Student ID number must be 5 digits.')
    if request.form['concern'] == "Select":
        is_valid = False
        flash('Choose a concern.')
    if request.form['intervention'] == "Select":
        is_valid = False
        flash('Choose an intervention.')
    if request.form['sstmember'] == "Select":
        is_valid = False
        flash('Choose an SST Member to supervise this intervention')
    if len(request.form['start']) < 1:
        is_valid = False
        flash('Choose a start date.')
    if len(request.form['checkin']) < 1:
        is_valid = False
        flash('Choose a start date.')
    start = datetime.strptime(request.form['start'], '%Y-%m-%d').date()
    checkin = datetime.strptime(request.form['checkin'], '%Y-%m-%d').date()
    today = datetime.now().date()
    if start < today:
        is_valid = False
        flash('Choose a start in the future.')
    if checkin < start:
        is_valid = False
        flash('Choose a checkin date after the start date.')

    if is_valid:
        # Validate that the id number belongs to a current student.
        match = Student.query.filter_by(STUDENT_NUMBER = request.form['studentid'], ENROLL_STATUS = 0).first()
        if match == None:
            is_valid = False
            flash('That ID was not found as an active student.')
            return redirect('/mtss/addint')
        else:
        # add to db
            # Get parameters
            treatid = Treatment.query.filter_by(treatment_name=request.form['intervention']).first()
            treatid = treatid.id
            sstid = Teacher.query.filter_by(LASTFIRST=request.form['sstmember']).first()
            sstid = sstid.TEACHERNUMBER
            sstid = SSTmember.query.filter_by(tchnum=sstid).first()
            sstid = sstid.id

            # Create intervention and commit
            new_int = Intervention(sstid=sstid, treatid=treatid, studentid=request.form['studentid'], startdate=start, checkin=checkin, status=0, concern_id=int(request.form['concern']))
            db.session.add(new_int)
            db.session.commit()

            
            if len(request.form['comment'])>0:
                # Create the comment and commit with new intervention ID
                comment = MTSScomment(sstid = session['userid'], studentid=new_int.studentid, intid=new_int.id, comment=request.form['comment'])
                db.session.add(comment)
                db.session.commit()
                commentid = comment.id

                # Add the comment ID to the intervention
                new_int.commentid = commentid
                db.session.commit()

            flash('Added')
            return redirect('/mtss/dashboard')

def endintconf(int_id):
    intervention = Intervention.query.filter_by(id=int(int_id)).first()
    outcomes = Outcome.query.all()
    user = SSTmember.query.filter_by(id=session['userid']).first()
    checks = MTSSchecks.query.filter_by(intid=intervention.id)
    startdate = intervention.startdate
    year = startdate[0:4]
    month = startdate[5:7]
    day = startdate[8:10]
    startdate = month + "/" + day + "/" + year
    return render_template ('endintconf.html', intervention=intervention, outcomes=outcomes, user=user, checks=checks, startdate=startdate)

def endint():
    if request.form['submit'] == "Cancel":
        return redirect ('/mtss/dashboard')
    intervention = Intervention.query.get(request.form['int_id'])
    intervention.status = 1
    intervention.outcome_id = int(request.form['intervention_outcome'])
    intervention.enddate = func.now()

    comment = MTSScomment(sstid = session['userid'], studentid=intervention.studentid, intid=intervention.id, comment=request.form['comment'])
    db.session.add(comment)
    db.session.commit()
    flash("Intervention Ended")
    return redirect('/mtss/dashboard')

def checkinview(int_id):
    intervention = Intervention.query.get(int(int_id))
    date = datetime.now() + timedelta(days=14)
    date = datetime.date(date)
    checks = MTSSchecks.query.filter_by(intid=intervention.id)
    otherints = Intervention.query.filter_by(studentid=intervention.studentid).all()
    user = SSTmember.query.filter_by(id=session['userid']).first()
    startdate = intervention.startdate
    year = startdate[0:4]
    month = startdate[5:7]
    day = startdate[8:10]
    startdate = month + "/" + day + "/" + year
    return render_template ('checkin.html', intervention = intervention, date=date, checks=checks, otherints=otherints, user=user, startdate=startdate)

def checkin():
    if request.form['submit'] == "Cancel":
        return redirect ('/mtss/dashboard')
    intervention = Intervention.query.get(int(request.form['int_id']))
    comment = MTSScomment(sstid = session['userid'], studentid=intervention.studentid, intid=intervention.id, comment=request.form['comment'])
    db.session.add(comment)
    db.session.commit()
    commentid = comment.id
    check = MTSSchecks(sstid=session['userid'], studentid=intervention.studentid, intid=intervention.id, commentid=commentid, nextcheck=request.form['nextcheck'])
    db.session.add(check)
    db.session.commit()
    comment.checkid = check.id
    intervention.checkin = request.form['nextcheck']
    db.session.commit()
    flash('The next check-in date has been updated and your comments have been added')
    return redirect ('/mtss/dashboard')