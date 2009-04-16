# coding: utf-8
import re

from google.appengine.ext import webapp
from google.appengine.api import mail
from util import render_template
import sha, random

from database import *

class FormRequestHandler(webapp.RequestHandler):
    """
    Extends Google App Engine's `webapp.RequestHandler` to add some form
    processing capabilities.
    """
    
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

class MainPage(webapp.RequestHandler):
    path = '/'
    
    def get(self):
        self.response.out.write(render_template('index.html'))

class Assignment(FormRequestHandler):
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
    
    def get(self):
        self.response.out.write(render_template('assignment.html', {
            'field_values': self.get_field_list(self.field_count),
            'min_values': 5,
        }))
        
    def post(self):
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
        
        has_enough_data = non_empty_field_count >= self.mandatory_field_count
        
        if has_enough_data:
            #TODO: place field_values in the database
            #TODO: make this a redirect
            self.response.out.write("The form was valid, and this should be a redirection to the next assignment.")
        else:
            field_values += self.get_field_list(self.field_count - non_empty_field_count, from_number=non_empty_field_count)
            
            self.response.out.write(render_template('assignment.html', {
                'field_values': field_values,
                'min_values': 5,
            }))

    
class Registration(FormRequestHandler):
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
        self.response.out.write(render_template('registration.html',{
                'members': self.get_members(),
            }))
        
    def get_members(self): return TempMember.gql("order by date desc")
        
    def post(self):
        # Data that is ready to be inserted into the database.
        self.clean_data = {}
        
        # Field specific errors where key is POSTed field name and the value
        # is the POSTed value.
        self.field_errors = {}
        
        self.run_validation_methods()
        
        if self.field_errors:
            # Display the form again if there were field errors.
            
            self.response.out.write(render_template('registration.html', {
                'errors': self.field_errors,
                'previous': self.request.POST,
                'members': self.get_members(),
            }))
        else:
            # create activation key
            password = self.request.get('password')
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+password).hexdigest()

            # insert into temp members table
            tmpMember = TempMember()
            tmpMember.name = self.clean_data['name']
            tmpMember.password = self.request.get('password')
            tmpMember.email = self.clean_data['email']
            tmpMember.age = int(self.clean_data['age'])
            tmpMember.gender = self.clean_data['gender']
            tmpMember.school = self.clean_data['school']
            tmpMember.postcode = int(self.clean_data['postal_code'])
            tmpMember.schoollvl = self.clean_data['class']
            tmpMember.activation_key = activation_key
            tmpMember.put()            
            
            # send confirmation email and inform the user of this
            #mail.send_mail(sender="support@hugmyndaraduneytid.is",
            #        to= tmpMember.email,
            #        subject="Staðfesta nýskráningu",
            #        body="""
            #                            
            #            Vinnsamlega fylgið meðfylgjandi hlekk til að virkja nýskráningu.
            #        
            #            Hugmyndaráðuneytið
            #            """)
            
            self.response.out.write(render_template('email_sent.html'))
            #TODO: Do something with `self.clean_data`.
            
            #self.redirect(Login.path)
            
    def validate_postal_code(self):
        postal_code = self.request.get('postal_code')
        
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
        
        if postal_code in valid_postal_codes:
            self.clean_data['postal_code'] = postal_code
        elif not postal_code:
            self.field_errors['postal_code'] = "Póstnúmer vantar."
        else:
            self.field_errors['postal_code'] = "Postnúmer er ekki rétt."
            
    def validate_name(self):
        name_regex = re.compile("^[\.\w'\- ]*$", re.UNICODE) # Sr. Eðvald O'Brien Kaplan-Moss
        name = self.request.get('name')
        
        if name_regex.match(name):
            self.clean_data['name'] = name
        else:
            self.field_errors['name'] = "Nafnið má innihalda bókstafi, ., ', - og bil."
        
    def validate_email(self):
        """Validate the e-mail address pattern and not whether it is active."""
        email = self.request.get('email')
        if mail.is_email_valid(email):
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
        age = self.request.get('age')
        if not age:
            self.field_errors['age'] = "Velja þarf aldur."
        elif age.isdigit():
            self.clean_data['age'] = age            
        else:
            self.field_errors['age'] = "Aldur er ekki réttur"
        
    def validate_gender(self):
        gender = self.request.get('gender')
        
        if gender:
            if gender in ('kk', 'kvk'):
                self.clean_data['gender'] = gender
            else:
                self.field_errors['gender'] = "Óþekkt snið á kyni."
        else:
            self.field_errors['gender'] = "Kyn vantar."
        
    def validate_school(self):
        school = self.request.get('school')
        self.clean_data['school'] = school
        
    def validate_class(self):
        klass = self.request.get('class')
        
        if klass == "empty":
            self.field_errors['class'] = "Bekkur ekki valinn."
        elif re.match("^([1-9]|10)\. bekkur$", klass):
            self.clean_data['class'] = klass
        else:
            self.field_errors['class'] = "Óþekkt snið fyrir bekk."
            
class Login(FormRequestHandler):
    path = '/login'
    
    def get(self):
        # TODO: checks
        #  1. does the user support cookies?
        #     - yes: continue
        #     - no: warn user, provide instructions
        #  2. is the user already logged in?
        #     - yes: redirect to post-logout page
        #     - no: display form
        
        self.response.out.write(render_template('login.html'))
        
    def post(self):
        # TODO: use checks from self.get
        
        self.response.out.write("To be done: Login processing.")
        
                
class Groups(FormRequestHandler):
    path = '/groups'
    
    def get_Groups(self): return Group.gql("ORDER BY date DESC")
    
    def get(self):
        # TODO: checks
        #  1. does the user support cookies?
        #     - yes: continue
        #     - no: warn user, provide instructions
        #  2. is the user already logged in?
        #     - yes: redirect to post-logout page
        #     - no: display form
        
        self.response.out.write(render_template('groups.html',{
            'groups': self.get_Groups(),
        }))
        
    def add_group(self):
        group = Group()
        group.name = self.request.get('name')
        group.put()
        
    def remove_member(self, email):
        q = Group.gql("Where email = :1", email)
        results = q.fetch(1)
        Group.delete(results)
        
    def add_member(self):
        group = Group()
        group.name = self.request.get('name')
        group.put()

    def post(self):
        if ( self.request.get('add_member') ): self.add_member()
        if ( self.request.get('remove_member') ) : self.remove_member()
        if ( self.request.get('add_group') )  : self.add_group()   
        
        self.redirect('/groups')
        
    
        