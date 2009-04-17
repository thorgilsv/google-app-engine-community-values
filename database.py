from google.appengine.ext import db
    
class TempMember(db.Model):
    name = db.StringProperty()
    password = db.StringProperty()
    email = db.EmailProperty()
    age = db.IntegerProperty()
    gender = db.StringProperty()
    school = db.StringProperty()
    postcode = db.IntegerProperty()
    schoollvl = db.StringProperty()
    validationcode = db.StringProperty()
    activation_key = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
  
class Assignments(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)
    name = db.StringProperty()
    question = db.StringProperty()
  
class Member(db.Model):
    name = db.StringProperty()
    password = db.StringProperty()
    email = db.EmailProperty()
    postcode = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    #we are storing the active assignment here 
    assignment = db.ReferenceProperty(Assignments) 
    
class Particpant(db.Model):
    member = db.ReferenceProperty(Member)
    age = db.IntegerProperty()
    gender = db.StringProperty()
    
class AssignmentAnswer(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)
    member = db.ReferenceProperty(Member)
    statement = db.StringProperty()
    current_state = db.IntegerProperty()
    headed_state = db.IntegerProperty()
    ideal_state = db.IntegerProperty()
    comment = db.StringProperty()
    answer_number = db.IntegerProperty()
    assignment = db.ReferenceProperty(Assignments)
    
class Essay(db.Model):
    member = db.ReferenceProperty(Member)
    text = db.TextProperty()

class Session(db.Model):
    session_key = db.StringProperty()
    member = db.ReferenceProperty(Member)
    expiry_time = db.DateTimeProperty()
    
