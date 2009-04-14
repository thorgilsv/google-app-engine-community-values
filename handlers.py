from google.appengine.ext import webapp

from util import render_template

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
    
    def get(self):
        self.response.out.write(render_template('assignment.html', {
            'field_list': range(10),
            'min_values': 5,
        }))
        
    def post(self):
        self.response.out.write(render_template('assignment.html', {
            'field_list': range(10),
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
        self.response.out.write(render_template('registration.html'))
        
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
                'previous': self.request.POST
            }))
        else:
            # Redirect to login if there were no field errors.
            
            #TODO: Do something with `self.clean_data`.
            
            self.redirect(Login.path)
            
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
        else:
            self.field_errors['postal_code'] = "Expected valid postal code."
            
    def validate_email(self):
        """Validate the e-mail address pattern and not whether it is active."""
        pass #TODO
        
    def validate_passwords(self):
        """Validate the password and password confirmation fields."""
        pass #TODO
        
    def validate_school(self):
        pass #TODO
        
    def validate_class(self):
        pass #TODO
            
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
        
        self.response.out.write('To be done: Login template.')
        
    def post(self):
        # TODO: use checks from self.get
        
        self.response.out.write("To be done: Login processing.")