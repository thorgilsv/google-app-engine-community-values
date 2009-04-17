# coding: utf-8
import re
import uuid

from google.appengine.ext import webapp
from google.appengine.api import mail
from util import render_template
import sha, random
from database import *
from django.contrib.sessions.models import Session
import session
import settings

class CustomRequestHandler(webapp.RequestHandler):
    """
    Extends Google App Engine's `webapp.RequestHandler` to add some form
    processing capabilities.
    """
    def render_to_response(self, template_name, context={}):
        """Render a template with request context common to all templates."""
        request_context = {
            'user': session.get_member(self),
        }
        
        # Merge contexts, overriding request context if clashing.
        request_context.update(context)
        
        self.response.out.write(render_template(template_name, context=request_context))
    
    def require_login(self):
        """Redirect to login if there's no active session."""
        #TODO: little time, but would be cooler as a decorator  
        if not session.get_session(self):
            self.redirect(Login.path)
    
    def run_prefixed_methods(self, prefix, *args, **kwargs):
        """
        Run all methods in this instance that start with a given prefix with
        given keyword arguments and arguments.
        
        Let's say you wanted all every method starting with `validate_` to
        run, you might create a couple of validation instance methods like
        so::
        
          def validate_email(self):
              email = self.POST['email']
              
              is_valid = True #this could be a real check
              
              if is_valid:
                  self.clean_data['email'] = email
              else:
                  self.field_errors['email'] = "Expected valid e-mail."
                  
        You'd then place `self.run_validation_methods('validate_')` in any and all
        methods that should run all 
        """
        
        # Get a list of all methods for this instance that start with `validate_`.
        validate_methods = [method for method in dir(self) if method.startswith(prefix)]
        for method in validate_methods:
            validate_result = getattr(self, method)(*args, **kwargs)

class MainPage(CustomRequestHandler):
    path = '/'
    
    def get(self):
        self.render_to_response('index.html', {'show_info_links': True})
        
class About(CustomRequestHandler):
    path = '/about'
    
    def get(self):
        self.render_to_response('about.html',{'show_info_links': True})
        
class Why(CustomRequestHandler):
    path = '/why'
    
    def get(self):
        self.render_to_response('why.html',{'show_info_links': True})       

class YourOpinion(CustomRequestHandler):
    path = '/your_opinion'
    
    def get(self):
        self.render_to_response('your_opinion.html',{'show_info_links': True})

class ForAll(CustomRequestHandler):
    path = '/for_all'
    
    def get(self):
        self.render_to_response('for_all.html',{'show_info_links': True})

class Society(CustomRequestHandler):
    path = '/society'
    
    def get(self):
        self.render_to_response('society.html',{'show_info_links': True})
        
class Values(CustomRequestHandler):
    path = '/values'
    
    def get(self):
        self.render_to_response('values.html',{'show_info_links': True})

class ProjectOwners(CustomRequestHandler):
    path = '/project_owners'
    
    def get(self):
        self.render_to_response('project_owners.html',{'show_info_links': True})

class Information(CustomRequestHandler):
    path = '/information'
    
    def get(self):
        self.render_to_response('information.html',{'show_info_links': True})

class Images(CustomRequestHandler):
    path = '/images'
    
    def get(self):
        self.render_to_response('images.html',{'show_info_links': True})

class Participation(CustomRequestHandler):
    path = '/participation'
    
    def get(self):
        self.render_to_response('participation.html',{'show_info_links': True})
        
class Assignment(CustomRequestHandler):
    #TODO: require login
    path = '/assignment'
    
    field_count = 10
    mandatory_field_count = 5
    
    def get_default_tuple(self, number):
        #TODO: change from tuple to class for dramatically increased readability
        return (number, '', '50', '50', '50')
    
    def get_field_list(self, count, from_number=0):
        """Return a tuple of default values."""
        return [self.get_default_tuple(from_number + number) for number in range(count)]
     
    def addAnswer(self, value, count, assignment):
        member = self.session.user 
        answer = value
        answer_number = count
        assignment = assignment
        
    def deleteAssignments(self):        
        q = db.GqlQuery("SELECT * FROM Assignments")
        results = q.fetch(10)
        db.delete(results)
        
    def createAssignments(self):
        t = Assignments()
        t.name = 'Verkefni 1'
        t.question = "Spurning1?" 
        t.put()
        t = Assignments()
        t.name = 'Verkefni 2'
        t.question = 'Spurning2?'        
        t.put()
        t = Assignments()
        t.name = 'Verkefni 3'
        t.question = 'Spurning3?'   
        t.put()        
        
    def getAssignments(self): return Assignments.gql("")
    
    def getAssignment(self,name):
        assignments = Assignments.gql("where name = :1",name)
        for each in assignments:
            return each
    
    def get(self):
        self.require_login()
        self.deleteAssignments()
        self.createAssignments()        
        
        self.render_to_response('assignment.html', {
            'field_values': self.get_field_list(self.field_count),
            'min_values': 5,
            'lvl': 'inner',
            'assignments': self.getAssignments(),
            'assignment': self.getAssignment(self.request.get('var')),
        })
        
    def post(self):
        self.require_login()
        
        #TODO: fix undercommenting
        field_values = []
        
        # Fill `field_values` with values of non-empty fields.
        for number in range(self.field_count):
            prefixes = ('value', 'current_state', 'headed_state', 'ideal_state')
            fields_tuple = tuple()
            
            for prefix in prefixes:
                field_name = '%s_%d' % (prefix, number)
            
                if field_name in self.request.POST:
                    fields_tuple += (self.request.POST[field_name],)
                else:
                    continue
            
            default_tuple = self.get_default_tuple(number)
            value_count = len(default_tuple[1:])
            
            #TODO: check that makes sure that value words are distinct -- any(...) class list
            
            if len(fields_tuple) != value_count:
                # Discard tuple if any fields are missing.
                continue
            elif fields_tuple == default_tuple[1:]:
                # Discard tuple if equal to default (empty).
                continue
            else:
                # If all fields are present, put it in the list of tuples.
                field_values.append((len(field_values),) + fields_tuple)
        
        non_empty_field_count = len(field_values)
        
        # Fill up the field_values tuple with empty fields to make up for the
        # ones that were empty or invalid. This way, non-empty fields will be
        # grouped together at the top.
        
        #we will always sav the values alreaddy submitted
        count=0
        for value in field_values:
                if value == None: break
                count+=1
                addAnswer(value, count, assignment)
        
        has_enough_data = non_empty_field_count >= self.mandatory_field_count
        
        if has_enough_data:
            #TODO: make this a redirect
            self.response.out.write("The form was valid, and this should be a redirection to the next assignment.")
        else:
            field_values += self.get_field_list(self.field_count - non_empty_field_count, from_number=non_empty_field_count)
            
            self.render_to_response('assignment.html', {
                'field_values': field_values,
                'min_values': 5,
                'lvl': 'inner',
            })

class Activation(CustomRequestHandler):
    """Activate a user that has already signed up."""
    path = "/activate"
    
    def get(self):
        activation_key = self.request.get('activation_key')
        
        # Some integrity assurance.
        temporary_member = TempMember.gql('WHERE activation_key = :1', activation_key).get()
        member = Member.gql('WHERE activation_key = :1', activation_key).get()
        
        if member:
            self.render_to_response('activation.html', {
                'member': member,
                'error': "Þessi notandi er þegar til virkjaður í kerfinu okkar.",
            })
        elif temporary_member:
            member = Member()
            
            member.password=temporary_member.password
            member.email=temporary_member.email
            member.age=temporary_member.age
            member.gender=temporary_member.gender
            member.school=temporary_member.school
            member.postcode=temporary_member.postcode
            member.schoollvl=temporary_member.schoollvl
            member.date=temporary_member.date
            
            # TODO: make put and delete atomic for integrity
            member.put()
            temporary_member.delete()
            
            self.render_to_response('activation.html', {
                'member': member,
            })
            
        else:
            self.render_to_response('activation.html', {
                'error': "Þessi þessi staðfestingartengill er ekki virkur.  Vinsamlega reyndu nýskráningu að nýju.",
            })
        
class Registration(CustomRequestHandler):
    """Register a group for it to be able to participate."""
    path = '/register'
    
    def run_validation_methods(self, *args, **kwargs):
        """
        Run all methods starting with `validate_` in this instance. Each of
        those methods is expected to add to `self.field_errors` and
        `self.clean_data` where appropriate.
        """
        
        self.run_prefixed_methods('validate_', *args, **kwargs)
        
    def get(self):
        self.render_to_response('registration.html', {
                'members': self.get_members(),                
            })
        
    def get_members(self): return Member.gql("order by date desc")
        
    def post(self):
        # Data that is ready to be inserted into the database.
        self.clean_data = {}
        
        # Field specific errors where key is POSTed field name and the value
        # is the POSTed value.
        self.field_errors = {}
        
        self.run_validation_methods()
        
        if self.field_errors:
            # Display the form again if there were field errors.
            
            self.render_to_response('registration.html', {
                'errors': self.field_errors,
                'previous': self.request.POST,
                'members': self.get_members(),
            })
        else:
                
            # insert into temp members table

            temporary_member = TempMember()
            temporary_member.name = self.clean_data['name']
            temporary_member.password = self.clean_data['password']
            temporary_member.email = self.clean_data['email']  
            temporary_member.age = self.clean_data['age']
            temporary_member.gender = self.clean_data['gender']
            temporary_member.activation_key = uuid.uuid4().hex
            temporary_member.put()            
            
            # To reduce the likelyhood of being caught by some SPAM filters, add a name if not empty.
            if temporary_member.name:
                to_line = "%s <%s>" % (temporary_member.name, temporary_member.email)
            else:
                to_line = temporary_member.email
            
            # end confirmation email and inform the user of this
            mail.send_mail(sender=settings.EMAIL_FROM,
                    to=to_line,
                    subject="Okkar framtíð: Staðfesting nýskráningar",
                    body="""Kæri viðtakandi,
                    
Takk fyrir að skrá þig í verkefnið Okkar framtíð.  Þú getur tekið
þátt í verkefninu með því að smella á tengilinn hér að neðan og
staðfesta þar með netfangið þitt.

http://%s/activate?activation_key=%s

Takk fyrir þátttökuna,
Hugmyndaráðuneytið""" % (settings.DOMAIN, temporary_member.activation_key) #TODO: improve writing
)
            
            self.render_to_response('email_sent.html', {'email': temporary_member.email })
            #TODO: Do something with `self.clean_data`.
                        
    def validate_postal_code(self):
        postal_code = self.request.get('postal_code').strip()
        
        valid_postal_codes = ('101', '102', '103', '104', '105', '107', '108',
        '109', '110', '111', '112', '113', '116', '121', '123', '124', '125',
        '127', '128', '129', '130', '132', '150', '155', '170', '172', '190',
        '200', '201', '202', '203', '210', '212', '220', '221', '222', '225',
        '230', '232', '233', '235', '240', '245', '250', '260', '270', '300',
        '301', '302', '310', '311', '320', '340', '345', '350', '355', '356',
        '360', '370', '371', '380', '400', '401', '410', '415', '420', '425',
        '430', '450', '451', '460', '465', '470', '471', '500', '510', '512',
        '520', '522', '523', '524', '530', '531', '540', '541', '545', '550',
        '551', '560', '565', '566', '570', '580', '600', '601', '602', '603',
        '610', '611', '620', '621', '625', '630', '640', '641', '645', '650',
        '660', '670', '671', '675', '680', '681', '685', '690', '700', '701',
        '710', '715', '720', '730', '735', '740', '750', '755', '760', '765',
        '780', '781', '785', '800', '801', '802', '810', '815', '820', '825',
        '840', '845', '850', '851', '860', '861', '870', '871', '880', '900',
        '902')
        
        if not postal_code or postal_code in valid_postal_codes:
            self.clean_data['postal_code'] = postal_code
        else:
            self.field_errors['postal_code'] = "Póstnúmer er ekki rétt."
            
    def validate_name(self):
        name_regex = re.compile("^[\.\w'\- ]*$", re.UNICODE) # Sr. Eðvald O'Brien Kaplan-Moss
        name = self.request.get('name')
        
        # name optional
        if name_regex.match(name) or name.strip() == '':
            self.clean_data['name'] = name
        else:
            self.field_errors['name'] = "Nafnið má innihalda bókstafi, ., ', - og bil."
        
    def validate_email(self):
        """Validate the e-mail address pattern and not whether it is active."""
        email = self.request.get('email')
        if mail.is_email_valid(email):
            if Member.gql('WHERE email = :1', email).get():
                self.field_errors['email'] = "Þetta netfang er þegar skráð í kerfið okkar."
            elif TempMember.gql('WHERE email = :1', email).get():
                self.field_errors['email'] = "Þetta netfang er skráð í kerfið okkar en hefur ekki verið virkjað.  Skoðaðu tölvupóstinn þinn og athugaðu hvort þér hefur borist staðfestingarpóstur."
            else:
                self.clean_data['email'] = email            
        else:
            self.field_errors['email'] = "Netfang er ekki rétt."
        
    def validate_passwords(self):
        """Validate the password and password confirmation fields."""
        password = self.request.get('password')
        password_confirm = self.request.get('password_confirm')
            
        if not password:
            self.field_errors['password'] = "Velja þarf lykilorð."
        elif password_confirm == password:
            self.clean_data['password'] = password
        else:
            self.field_errors['password'] = "Lykilorðin þurfa að vera eins."
            
    def validate_age(self):
        age = self.request.get('age').strip()
        if not age:
            self.clean_data['age'] = None
        elif age.isdigit():
            self.clean_data['age'] = int(age)
        else:
            self.field_errors['age'] = "Aldur er ekki réttur."
        
    def validate_gender(self):
        gender = self.request.get('gender', '')
        
        if not gender:
            self.clean_data['gender'] = None
        elif gender in ('kk', 'kvk'):
            self.clean_data['gender'] = gender
        else:
            self.field_errors['gender'] = "Óþekkt snið á kyni."

class Login(CustomRequestHandler):
    path = '/login'
    
    def get(self):
        # TODO: do cookie support check
        
        self.render_to_response('login.html',{
            'show_info_links': True,
            'user': session.get_member(self)
        })
                
    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')       
         
        members = Member.gql("where email = :1 and password = :2 ", email, password)
        member = members.get()
        
        if member:
            session.login(self, member)
            self.redirect(Assignment.path)
        else:
            self.render_to_response('login.html',{
                'show_info_links': True,
                'error': 'Annaðhvort netfang eða lykilorð er rangt.',
            })
                
class Logout(CustomRequestHandler):
    path = '/logout'
    
    def get(self):
        session.logout(self)
        self.redirect(Login.path)
        
    def post(self):
        self.get()