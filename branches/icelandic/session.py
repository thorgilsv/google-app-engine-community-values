import uuid

from database import Session
import settings
from datetime import datetime, timedelta

def get_session(request_handler):
    """Get the session entity for the requesting user or return None."""
    if 'session_key' in request_handler.request.cookies:
        key = request_handler.request.cookies['session_key']
        sessions = Session.all()
        sessions = sessions.filter('session_key = ', key)
        # TODO: filter out expired sessions
        
        session = sessions.get()
        
        return session
    else:
        return None

def get_member(request_handler):
    """Get the member object affiliated with the current request or return None."""
    
    session = get_session(request_handler)
    
    if session:
        return session.member
    else:
        return None
        
def login(request_handler, member):
    """Log the current requester in as `member`."""
    logout(request_handler)
    
    session_key = uuid.uuid4().hex
    expiry_time = datetime.now() + timedelta(seconds=settings.SESSION_EXPIRY)
    new_session = Session(member=member, session_key=session_key, expiry_time=expiry_time)
    new_session.put()
    
    request_handler.response.headers['Set-Cookie'] = "session_key=%s" % session_key
    
def logout(request_handler):
    """Remove the current user from the session database."""
    
    # TODO: delete cookie, (set again with expires time in the past)
    session = get_session(request_handler)

    if session:
        session.delete()