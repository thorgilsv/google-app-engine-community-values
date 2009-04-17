from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


from handlers import *
                  
application = webapp.WSGIApplication([
        (Registration.path, Registration),
        (Login.path, Login),
        (Assignment.path, Assignment),
        (About.path, About),
        (Why.path, Why),
        (YourOpinion.path, YourOpinion),
        (ForAll.path, ForAll),
        (Society.path, Society),
        (Values.path, Values),
        (ProjectOwners.path, ProjectOwners),
        (Information.path, Information),
        (Images.path, Images),
        (Participation.path, Participation),
        (Logout.path, Logout),
        #(Answer.path, Answer), #fridrik had to disable because it broke my build; Answer does not exist in handlers
        (Activation.path, Activation),
    ], debug = True)


def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()
