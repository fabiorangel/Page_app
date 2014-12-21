def index():

    from gluon.tools import geocode

    #Getting info from form
    req = request.vars.location
    if(req != None):
        coordenadas = geocode('%s' % req)
    else:
        coordenadas = geocode('%s' % "NUIG")

    #Getting Tweets from Twitter
    import oauth2 as oauth
    import json
    import time
    import urllib
    import pymongo

    CONSUMER_KEY = "05Bgk2UtKQ5Pfd8wSeY0oQ"
    CONSUMER_SECRET = "ADhhRsEy75X81Nv87KZ5ywuWEpDrGi2ur6GeZuKrYzk"
    ACCESS_KEY = "2162977602-9cJ8nXY0prz2PeESWShKNlapDk46gZaTIh4RqqE"
    ACCESS_SECRET = "fgfrG95dRnNJMQ0lnZRmq9ImxMFlVTmXl2UuDPiRRgY9L"

    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    client = oauth.Client(consumer, access_token)

    q = request.vars.location
    tweet_arr = []
    working = 1
    if(q != None):
        try:
            q = urllib.quote(str(q))
            URL = "https://api.twitter.com/1.1/search/tweets.json?q="+str(q)+"&count=5"
            response, data = client.request(URL, "GET")
            tweets = json.loads(data)

            for tweet in tweets['statuses']:
                tweet_arr.append(tweet)
        except Exception, e:
            working = 0

    else:
        working = 0

    #getting DBpedia info
    import xml.etree.ElementTree as ET
    import urllib2
    description = ""
    query = ""
    try:
        if(q != None):
            URL = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryClass=place&QueryString="+q

            r = urllib2.Request(URL)
            f = urllib2.urlopen(r)
            tree = ET.parse(f)
            root = tree.getroot()
            description = root[0][2].text
            query = root[0][0].text
            dbpedia_url = root[0][1].text
    except:
        query = q
        description = "Sorry. DBpedia has no information about "+q+"."

    return dict(coordenadas=coordenadas,tweet_arr=tweet_arr,working=working,description=description,query=query)

#framework auto Generated code
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
