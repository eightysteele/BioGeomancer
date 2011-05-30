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
