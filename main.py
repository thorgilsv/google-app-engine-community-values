from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from handlers import MainPage, Registration, Login, Assignment
                  
application = webapp.WSGIApplication([
        (MainPage.path, MainPage),
        (Registration.path, Registration),
        (Login.path, Login),
        (Assignment.path, Assignment),
    ], debug = True)

def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()
