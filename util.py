import os

from google.appengine.ext.webapp import template

def render_template(template_name, context={}):
    """
    Return a string where a template has been processed with variables given
    in `context`.
    
    The template name should be the name of a template relative to the
    /templates directory in the root. For example, for a template located in
    /templates/registration.html, the given `template` name would be
    `registration.html`.
    """
    
    path = os.path.join(os.path.dirname(__file__), 'templates', template_name)
    return template.render(path, context)