import cgi
from getpass import getpass
from google.appengine.api import urlfetch, mail, memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import os
import simplejson
import logging
import urllib
import urllib2
try:
    import json
except ImportError:
    from django.utils import simplejson as json

import geomancer

# ==============================================================================
# Google Prediction API

class GooglePredictionApi(object):

    @staticmethod
    def GetAuthentication(email, password):
        """Retrieves a Google authentication token.
        """
        url = 'https://www.google.com/accounts/ClientLogin'
        post_data = urllib.urlencode([
                ('Email', email),
                ('Passwd', password),
                ('accountType', 'HOSTED_OR_GOOGLE'),
                ('source', 'companyName-applicationName-versionID'),
                ('service', 'xapi'),
                ])
        result = urlfetch.fetch(url=url, payload=post_data, method=urlfetch.POST)
        content = '&'.join(result.content.split())
        query = cgi.parse_qs(content)
        auth = query['Auth'][0]
        logging.info('Auth: ' + auth)
        return auth

    @staticmethod
    def Predict(auth, model, query):
        url = ('https://www.googleapis.com/prediction/v1.1/training/'
               '%s/predict' % urllib.quote(model, ''))
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'GoogleLogin auth=%s' % auth,
            }
        post_data = GooglePredictionApi.GetPostData(query)
        logging.info('Post Data: '+ str(post_data))
        result = urlfetch.fetch(url=url, payload=post_data, method=urlfetch.POST, headers=headers)
        content = result.content
        logging.info('Content: ' + content)
        json_content = json.loads(content)['data']

        scores = []
        print json.loads(content)
        # classification task
        if 'outputLabel' in json_content:
            prediction = json_content['outputLabel']
            jsonscores = json_content['outputMulti']
            scores = GooglePredictionApi.ExtractDictScores(jsonscores)
        # regression task
        else:
            prediction = json_content['outputValue']

        return [prediction, scores]

    @staticmethod
    def ExtractDictScores(jsonscores):
        scores = {}
        for pair in jsonscores:
            for key, value in pair.iteritems():
                if key == 'label':
                    label = value
                elif key == 'score':
                    score = value
            scores[label] = score
        return scores

    @staticmethod
    def GetPostData(query):
        data_input = {}
        data_input['mixture'] = [query]

        post_data = json.dumps({
                'data': {
                    'input': data_input
                    }
                })
        return post_data

# ===============================================================================
# Request handlers

class BaseHandler(webapp.RequestHandler):
    def render_template(self, file, template_args):
        path = os.path.join(os.path.dirname(__file__), "html", file)
        self.response.out.write(template.render(path, template_args))

    def push_html(self, file):
        path = os.path.join(os.path.dirname(__file__), "html", file)
        self.response.out.write(open(path, 'r').read())

class LocalityTypeApi(BaseHandler):
    EMAIL = ''
    PASSWORD = ''
    def get(self):
        self.post()

    def post(self):
        query = self.request.get('q')
        results = self.predict(query)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(results)
        
    @classmethod
    def predict(cls, query):
        results = memcache.get(query)
        if not results:
            auth = GooglePredictionApi.GetAuthentication('eightysteele@gmail.com', '')
            model = 'biogeomancer/locs.csv'
            results = simplejson.dumps(GooglePredictionApi.Predict(auth, model, query))
            memcache.add(query, results)
        return results

class GeoreferenceApi(BaseHandler):
    def get(self):
        return self.post()

    def post(self):
        locality = self.request.get('q')
        params = urllib.urlencode([('address', locality), ('sensor', 'false')])
        url = 'http://maps.googleapis.com/maps/api/geocode/json?%s' % params
        geocode = simplejson.loads(urlfetch.fetch(url).content)
        georef = geomancer.georef(geocode)
        if georef is None:
            loctype = LocalityTypeApi.predict(locality)[0]
            georef = geomancer.georef(geocode, loctype)
        

class RootHandler(BaseHandler):
    def get(self):
        self.push_html("georef.html")

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
         [('/', RootHandler),
          ('/api/georeference', GeoreferenceApi),
          ('/api/localities/type', LocalityTypeApi),
          ('/hooks/post-commit', GitHubPostReceiveHooksHandler), ],
         debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
