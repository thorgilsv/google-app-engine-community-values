from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from handlers import MainPage, Registration, Login, Assignment, Groups
                  
application = webapp.WSGIApplication([
        (MainPage.path, MainPage),
        (Registration.path, Registration),
        (Login.path, Login),
        (Assignment.path, Assignment),
        (Groups.path, Groups),
    ], debug = True)

def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()
