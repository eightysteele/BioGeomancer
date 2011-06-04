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
from geomancer import Locality

class GoogleGeocodeApi(object):
    
    @classmethod    
    def execute(cls, locality):
        """Executes geocode request for locality and returns response object."""
        mkey = 'geocode-%s' % locality
        result = memcache.get(mkey)
        if not result:
            params = urllib.urlencode([('address', locality), ('sensor', 'false')])
            url = 'http://maps.googleapis.com/maps/api/geocode/json?%s' % params
            result = simplejson.loads(urlfetch.fetch(url).content)
            memcache.add(mkey, result)
        return result
        
    @classmethod
    def ispartialmatch(cls, result):
        """Returns true if the geocode result was a partial match."""
        return result.has_key('partial_match') and \
               result.get('partial_match') is True

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
    AUTH = None

    def get(self):
        self.post()

    def post(self):
        query = self.request.get('q')
        results = simplejson.dumps(self.predict(query))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(results)
        
    @classmethod
    def predict(cls, query):
        mkey = 'predict-%s' % query
        results = memcache.get(mkey)
        if not results:
            if not cls.AUTH:
                cls.AUTH = GooglePredictionApi.GetAuthentication('eightysteele@gmail.com', '')
            model = 'biogeomancer/locs.csv'
#            model = 'tuco-geomancer/CALocsForPrediction.csv'
            results = GooglePredictionApi.Predict(cls.AUTH, model, query)
            memcache.add(mkey, results)
        return results

class GeoreferenceApi(BaseHandler):
    def get(self):
        return self.post()

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        q = self.request.get('q')
        mkey = 'georef-%s' % q

        result = memcache.get(mkey)
        if result:
            logging.info('RESULT ' + str(result))
            self.response.out.write(simplejson.dumps(result))
            return

        geocode = GoogleGeocodeApi.execute(q)
        status = geocode.get('status')
        if status != 'OK':
            self.error(400)
            self.response.out.write('Unable to georeference %s (%s)' % (q, geocode.get('status')))
            return
        if GoogleGeocodeApi.ispartialmatch(geocode.get('results')[0]):
            # partial match requires prediction and further processing
            loctype = LocalityTypeApi.predict(q)[0]
            if loctype == 'foh':
#                meters = ['m', 'm.', 'meter', 'meters', 'mts', 'mts.', 'metre', 'metres']
#                west = ['w', 'w.', 'west', 'western', 'w 1/2']
                tokens = [x.strip().lower() for x in q.split() if x not in ['of']]

                offsetunit = None
                offsetval = None
                heading = None
                feature = None

                for token in tokens:
                    if token.isdigit():
                        # TODO: fails for tokens that are distances as words (five).
                        #       and tokens that consist of mixed numbers (5 1/2)
                        offsetval = token
                        continue
                    if geomancer.get_unit(token):
                        # TODO: fails for tokens that consist of more than one word (nautical miles).
                        offsetunit = token
                        continue
                    if geomancer.get_heading(token):
                        # TODO: fails for tokens that look like directions but are part of the name (South Haven).
                        heading = token
                        continue
                    # TODO: Fails for features consisting of more than one word (Los Altos)
                    feature = token
                # If the the component parts are all here, can't georeference.
                if not offsetunit:
                    self.error(400)
                    self.response.out.write('Unable to georeference %s as %s, missing offset unit' % (q, loctype) )
                    return
                if not offsetval:
                    self.error(400)
                    self.response.out.write('Unable to georeference %s as %s, missing offset value' % (q, loctype) )
                    return
                if not heading:
                    self.error(400)
                    self.response.out.write('Unable to georeference %s as %s, missing heading value' % (q, loctype) )
                    return
                if not feature:
                    self.error(400)
                    self.response.out.write('Unable to georeference %s as %s, missing feature value' % (q, loctype) )
                    return
                parts = {
                    'locality': q,
                    'locality_type': loctype,
                    'offset_unit': offsetunit,
                    'offset_value': offsetval,
                    'heading': heading,
                    'feature': {
                        'name': feature,
                        'geocode': GoogleGeocodeApi.execute(feature)
                        }
                    }                
                logging.info('parts: %s'%(parts))
                locality = Locality(q, loctype=loctype, parts=parts, geocode=geocode)
                georef = geomancer.georeference(locality)
                logging.info('georef: %s'%(georef))
                result = {
                    'interpretation': parts,
                    'georeference':
                        {
                        'error':georef.error, 
                        'lat':georef.point[1], 
                        'lng':georef.point[0]
                        }
                    }
                memcache.add(mkey, result)
                self.response.out.write(simplejson.dumps(result))
                return

            result = {
                'locality': {
                    'name': q,
                    'type': loctype
                    },
                'status': '%s not implemented' % loctype
                }
            memcache.add(mkey, result)
            self.response.out.write(simplejson.dumps(result))
            return

        locality = Locality(q, geocode=geocode)
        georef = geomancer.georeference(locality)
        result = {
            'locality': q,
            'georeference':
                {
                'error':georef.error, 
                'lat':georef.point.lat, 
                'lng':georef.point.lng
                }
            }
        memcache.add(mkey, result)
        self.response.out.write(simplejson.dumps(result))

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
