from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from handlers import MainPage, Registration, Login
                  
application = webapp.WSGIApplication([
        (MainPage.path, MainPage),
        (Registration.path, Registration),
        (Login.path, Login),
    ], debug = True)

def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()
