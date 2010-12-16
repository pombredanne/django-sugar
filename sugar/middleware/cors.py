from django.conf import settings

class CORSMiddleware(object):
    """
    Middleware that serves up representations with a CORS header to
    allow third parties to use your web api from JavaScript without 
    requiring them to proxy it.
    See: http://www.w3.org/TR/cors/

    Implement
    ---------
    Add to your middleware:

    'sugar.middleware.cors.CORSMiddleware',

    This will inject all your 'application/json' responses with:

        Access-Control-Allow-Origin: *

    Optionally you can configure the mediatypes you'd like to have be served 
    up with CORS in your settings:

    CORS = [ 
            "{
                ["application/json", "application/x-suggestions+json"],
                "Access-Control-Allow-Origin": "*" 
            }
           ]
           hmmm... not sure what to do here (yet)

    """

    def __init__(self):
        # should any others be added here?
        self.json_mediatypes = ["application/json"]

    def process_response(self, request, response):
        # just get the mediatype (strip charset)
        mediatype = response.get('content-type', '').split(";")[0].lower()
        if mediatype in self.json_mediatypes:
            response['Access-Control-Allow-Origin'] = '*'
        return response
