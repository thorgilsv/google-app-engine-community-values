
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
  
class Member(db.Model):
    name = db.StringProperty()
    password = db.StringProperty()
    email = db.EmailProperty()
    age = db.IntegerProperty()
    gender = db.StringProperty()
    school = db.StringProperty()
    postcode = db.IntegerProperty()
    schoollvl = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
  
  
class Group(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)
    name = db.StringProperty()
    mamber = db.ReferenceProperty(Member)
    
class GroupMember(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)
    group = db.ReferenceProperty(Group)
    member = db.ReferenceProperty(Member)