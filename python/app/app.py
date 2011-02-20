from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import os
import simplejson
import logging
from google.appengine.api import mail

# ===============================================================================
# Request handlers

class BaseHandler(webapp.RequestHandler):
    def render_template(self, file, template_args):
        path = os.path.join(os.path.dirname(__file__), "templates", file)
        self.response.out.write(template.render(path, template_args))

class GitHubPostReceiveHooksHandler(BaseHandler):    
    def post(self):
        payload = self.request.get('payload')
        json = simplejson.loads(payload)
        title = '[%s] New GitHub activity - GIT push' % json['repository']['name']
        body = 'The following commits were just pushed:\n\n'
        for c in json['commits']:
            body += '%s\n' % c['message']
            body += '%s (author)\n' % c['author']['name']
            body += '%s\n' % c['timestamp']
            body += '%s\n\n' % c['url']
        logging.info(body)
        mail.send_mail(sender="BioGeomancer <admin@biogeomancer.appspotmail.com>",
              to="Aaron <eightysteele@gmail.com>, John <tuco@berkeley.edu>",
              subject=title,
              body=body)        
        
application = webapp.WSGIApplication(
         [('/hooks/post-commit', GitHubPostReceiveHooksHandler), ],
         debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
