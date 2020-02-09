from sqlalchemy.sql import func
from config import db


# CLASSES (alpha order)
class Caregiver(db.Model):   #Somebody who administers a treatment to a student, ie a specific tutor.
    __tablename__ = "caregivers"
    id = db.Column(db.Integer, primary_key=True)
    tchnum = db.Column(db.Integer)
    treat_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())  
    modified_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Concern(db.Model):	# A reason a student would be put into intervention.
    __tablename__ = "mtss_concerns"   		
    id = db.Column(db.Integer, primary_key=True)
    concern_name = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())  
    modified_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


class Intervention(db.Model):  # A specific instance of intervening on a student.  There would be a Concern associated with a student, where and SST member would schedule a caregiver to adminster a treatment.
    __tablename__ = "interventions"
    id = db.Column(db.Integer, primary_key=True)
    sstid = db.Column(db.Integer, db.ForeignKey("SSTmembers.id", ondelete="cascade"), nullable=False)
    supervisor = db.relationship('SSTmember', foreign_keys=[sstid], backref="supervisor")
    studentid = db.Column(db.Integer, db.ForeignKey("Wrk_Students.STUDENT_NUMBER", ondelete="cascade"), nullable=False)
    student = db.relationship('Student', foreign_keys=[studentid], backref="student")
    treatid = db.Column(db.Integer, db.ForeignKey("treatments.id", ondelete="cascade"), nullable=False)
    treatment = db.relationship('Treatment', foreign_keys=[treatid], backref="treatment")
    startdate = db.Column(db.DateTime)
    enddate = db.Column(db.DateTime)
    checkin = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=func.now())  
    modified_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    status = db.Column(db.Integer)
    student = db.relationship('Student', foreign_keys=[studentid], backref="Student")
    outcome_id = db.Column(db.Integer, db.ForeignKey("mtss_outcomes.id", ondelete="cascade"), nullable=False)
    outcome = db.relationship('Outcome', foreign_keys=[outcome_id], backref="outcome")
    concern_id = db.Column(db.Integer, db.ForeignKey("mtss_concerns.id", ondelete="cascade"), nullable=False)
    concern = db.relationship('Concern', foreign_keys=[concern_id], backref="concern")

class MTSSchecks(db.Model): # A record of when a student was checked on by staff
    __tablename__ = "mtss_checks"
    id = db.Column(db.Integer, primary_key=True)
    sstid = db.Column(db.Integer)
    studentid = db.Column(db.Integer)
    intid = db.Column(db.Integer)
    commentid = db.Column(db.Integer, db.ForeignKey('mtss_comments.id', ondelete="cascade"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())  
    modified_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    nextcheck = db.Column(db.DateTime)
    checkcom = db.relationship('MTSScomment', foreign_keys=[commentid], backref="checkcom")

class MTSScomment(db.Model):   # Comments made about students or their progress
    __tablename__ = "mtss_comments"
    id = db.Column(db.Integer, primary_key=True)
    sstid = db.Column(db.Integer)
    studentid = db.Column(db.Integer)
    intid = db.Column(db.Integer)
    comment = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())  
    modified_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    checkid = db.Column(db.Integer)


class Outcome(db.Model):  # An outcome is a status assigned to an intervention when it is ended.
    __tablename__ = "mtss_outcomes"
    id = db.Column(db.Integer, primary_key=True)
    outcome_name = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())  
    modified_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class SSTmember(db.Model):  # A member of the SST team who may monitor or work with certain students
    __tablename__ = "SSTmembers"
    id = db.Column(db.Integer, primary_key=True)
    tchnum = db.Column(db.Integer, db.ForeignKey("Wrk_teachers.TEACHERNUMBER", ondelete="cascade"), nullable=False)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())  
    modified_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    ts_id = db.Column(db.String(255))
    email = db.Column(db.String(255))
    pw = db.Column(db.String(255))
    teacher = db.relationship('Teacher', foreign_keys=[tchnum], backref="teacher")

class Student(db.Model):
    __tablename__ = "Wrk_Students"
    id = db.Column(db.Integer, primary_key=True)
    STUDENT_NUMBER = db.Column(db.Integer)
    LASTFIRST = db.Column(db.String(255))
    ENROLL_STATUS = db.Column(db.String(2))
    FIRST_NAME = db.Column(db.String(255))
    LAST_NAME = db.Column(db.String(255))



class Treatment(db.Model):  # What the school offers to help a student address a concern.
    __tablename__ = "treatments"
    id = db.Column(db.Integer, primary_key=True)
    treatment_name = db.Column(db.String(100))
    status = db.Column(db.Integer)
    treatment_type = db.Column(db.String(255))
    need = db.Column(db.String(200))
    standard_duration = db.Column(db.Integer)
    rti_tier = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())  
    modified_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Teacher(db.Model):  # Wrk_teachers from SQL.Assessment
    __tablename__ = "Wrk_teachers"
    id = db.Column(db.Integer, primary_key=True)
    TEACHERNUMBER = db.Column(db.Integer)
    LASTFIRST = db.Column(db.String(255))
    FIRST_NAME = db.Column(db.String(255))
    LAST_NAME = db.Column(db.String(255))
    EMAIL_ADDR = db.Column(db.String(255))
