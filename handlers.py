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
    
    def set_cookie(self, key, value):
        """Send an HTTP header that sets a user's cookie."""
        self.response.headers['Set-Cookie'] = "%s=%s" % (key, value)
        
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

class Essay(CustomRequestHandler):
    path = '/essay'
    
    def get(self):
        

class Assignment(CustomRequestHandler):
    #TODO: require login
    path = '/assignment'
    
    field_count = 10
    mandatory_field_count = 1
    
    def get_default_tuple(self, number):
        #TODO: change from tuple to class for dramatically increased readability
        return (number, '', '3', '3', '3', '')
    
    def get_field_list(self, count, from_number=0):
        """Return a tuple of default values."""
        return [self.get_default_tuple(from_number + number) for number in range(count)]
     
    def addAnswer(self, value, assignment):
        t.member = session.get_member(self)
        t.statement = value[1]
        t.current_state = int(value[2])
        t.headed_state = int(value[3])
        t.ideal_state = int(value[4])
        t.comment = value[5]
        t.answer_number = value[0]
        t.assignment = assignment
        t.put()
                
    def get_answers(self):
        Assignment.gql("WHERE assignment = :1 AND member = :2", self.get_current_assignment(), session.get_member(self))
        
    def deleteAssignments(self):        
        q = db.GqlQuery("SELECT * FROM Assignments")
        results = q.fetch(10)
        db.delete(results)
        
    def createAssignments(self):
        t = Assignments()
        t.name = 'Verkefni 1'
        t.question = "O hai 1." 
        t.put()
        t = Assignments()
        t.name = 'Verkefni 2'
        t.question = 'O hai 2.'        
        t.put()   
        
    def getAssignments(self): return Assignments.gql("order by name asc")
    
    def getAssignment(self, name):
        assignments = Assignments.gql("where name = :1", name)
        return assignments.get()
        
    def getDefaultAssignment(self):
        member = session.get_member(self)
        if member.assignment: return member.assignment
        
        assignments = Assignments.gql("order by name asc")
        return assignments.get()
        
    def getAnswers(self,assignment):
        return AssignmentAnswer.gql("where assignment = :1 and member = :2 order by answer_number asc", assignment, session.get_member(self))
    
    def getAnswer(self, assignment, number):
        q = AssignmentAnswer.gql("where assignment = :1 and member = :2 and answer_number = :3 ", assignment, session.get_member(self), number)
        return q.get()
    
    def get_current_assignment(self):
        return self.getAssignment(self.request.get('var'))
        
    def updateUser(self,assignment):
        member = session.get_member(self)
        member.assignment = assignment
        member.put()
        
    def get_answer_tuples(self, answers):
        
        tuple_list = []
        
        for answer in answers:
            tuple_list.append((answer.answer_number, answer.statement, answer.current_state, answer.headed_state, answer.ideal_state, answer.comment))
        
        return tuple_list
        
    def get(self):
        self.require_login()
        assignment_name = self.request.get('var')
        if assignment_name:
            assignment = self.getAssignment(assignment_name)
        else:
            assignment = self.getDefaultAssignment()
            
        self.updateUser(assignment)
        
        #TODO fill inn stored answers
        answers = self.getAnswers(assignment)
        member = session.get_member(self)
        assignment_answers = AssignmentAnswer.gql("where assignment = :1 and member = :2 order by answer_number asc", member.assignment, member)
        field_values = self.get_answer_tuples(assignment_answers)
        
        non_empty_field_count = assignment_answers.count()
        field_values += self.get_field_list(self.field_count - non_empty_field_count, from_number=non_empty_field_count+1)
                        
        self.render_to_response('assignment.html', {
            'field_values': field_values,
            'choice_names': ('Slæm','Slöpp','Þokkaleg','Ágæt','Fín'),
            'min_values': 5,
            'assignments': self.getAssignments(),
            'assignment': assignment,
            'user': session.get_member(self),
        })
        
    def post(self):
        self.require_login()
        
        #TODO: fix undercommenting
        field_values = []
                
        # Fill `field_values` with values of non-empty fields.
        for number in range(self.field_count):
            prefixes = ('value', 'current_state', 'headed_state', 'ideal_state', 'comment')
            fields_tuple = tuple()
            
            for prefix in prefixes:
                field_name = '%s_%d' % (prefix, number+1)
                
                if field_name in self.request.POST:
                    field_value = self.request.POST[field_name]
                    
                    # The 'value' field is mandatory, skip if empty.
                    if prefix == 'value' and not field_value:
                        continue
                        
                    fields_tuple += (field_value,)
                else:
                    continue
            
            default_tuple = self.get_default_tuple(number+1)
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
                field_values.append((len(field_values)+1,) + fields_tuple)
        
        non_empty_field_count = len(field_values)
        
        # Fill up the field_values tuple with empty fields to make up for the
        # ones that were empty or invalid. This way, non-empty fields will be
        # grouped together at the top.

        member = session.get_member(self) # session.get_member('assignment')
        #we will always save the values already submitted        
        
        previous_answers = AssignmentAnswer.gql("WHERE member = :1 AND assignment = :2", member, member.assignment)
        for answer in previous_answers:
            answer.delete()
        
        for value in field_values:
            if value == None: break
            self.addAnswer(value, member.assignment)
        
        has_enough_data = non_empty_field_count >= self.mandatory_field_count
        

        if has_enough_data and self.request.get('completed'):
            #redirect to show answers
            self.redirect(Answer.path)
            
        elif self.request.get('foobar') :
            #the user is logging of for now
            self.redirect(Logout.path)
        else:
            self.get()


class Answer(CustomRequestHandler):
    path = '/answers'
    
    def getAnswers(self):
        member = session.get_member(self)
        return AssignmentAnswer.gql("where assignment = :1 and member = :2 order by answer_number asc", member.assignment, member)
        
    def getAssignments(self): return Assignments.gql("order by date asc")
    
    def get(self):
        self.require_login()
        member = session.get_member(self)
        self.response.out.write(render_template('answer.html',{            
            'assignments': self.getAssignments(),
            'answers': self.getAnswers(),
            'user': session.get_member(self)
            }))


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
    path = '/'
    
    def run_validation_methods(self, *args, **kwargs):
        """
        Run all methods starting with `validate_` in this instance. Each of
        those methods is expected to add to `self.field_errors` and
        `self.clean_data` where appropriate.
        """
        
        self.run_prefixed_methods('validate_', *args, **kwargs)
        
    def get(self):
        if session.get_member(self):
            self.redirect(Assignment.path)
        else:
            self.render_to_response('registration.html', {
                    'members': self.get_members(),                
                })
        
    def get_members(self): return Member.gql("order by date desc")
    
    def sendForgottenPassword(self,email):
        q = Member.gql("where email = :1", email)
        member = q.get()
                    
        if not member: return
        # send password in email
        
        mail.send_mail(sender=settings.EMAIL_FROM,
                    to=email,
                    subject="Framtíðarsýn þjóðar: Gleymt lykilorð",
                    body="""Kæri viðtakandi,
                    
                            Lykilorð þitt er '%s'
                            
                            Takk fyrir þátttökuna,
                            Hugmyndaráðuneytið""" % member.password.__str__()
                        )       
        
        
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
                'user': session.get_member(self)
            })
        else:
                
            # insert into temp members table

            temporary_member = TempMember()
            temporary_member.name = self.clean_data['name']
            temporary_member.password = self.clean_data['password']
            temporary_member.email = self.clean_data['email']  
            temporary_member.age = self.clean_data['age']
            temporary_member.gender = self.clean_data['gender']
            temporary_member.postcode = int(self.clean_data['postal_code'])
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
                    subject="Framtíðarsýn þjóðar: Staðfesting nýskráningar",
                    body="""Kæri viðtakandi,
                    
            Takk fyrir að skrá þig í verkefnið Framtíðarsýn þjóðar.  Þú getur tekið
            þátt í verkefninu með því að smella á tengilinn hér að neðan og
            staðfesta þar með netfangið þitt.
            
            http://%s/activate?activation_key=%s
            
            Takk fyrir þátttökuna,
            Hugmyndaráðuneytið""" % (settings.DOMAIN, temporary_member.activation_key) #TODO: improve writing
            )
            

            self.render_to_response('email_sent.html', {'email': temporary_member.email })

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
        
        if not postal_code:
            self.field_errors['postal_code'] = "Velja þarf póstnúmer."
        elif postal_code in valid_postal_codes:
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
            if self.request.get('gleymt'): self.sendForgottenPassword(email)
            elif Member.gql('WHERE email = :1', email).get():
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
            self.field_errors['password_confirm'] = "Lykilorðin þurfa að vera eins."
            
    def validate_age(self):
        age = self.request.get('age').strip()
        if not age:
            self.clean_data['age'] = None
        elif age.isdigit():
            self.clean_data['age'] = int(age)
        else:
            self.field_errors['age'] = "Aldur er ekki réttur."
        
    def validate_gender(self):
        self.clean_data['gender'] = self.request.get('gender', '')

class CookieTest(CustomRequestHandler):
    path = '/cookietest'
    
    def get(self):
        self.set_cookie('test_cookie', 'SUCCESS')
        #TODO: finish :)

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