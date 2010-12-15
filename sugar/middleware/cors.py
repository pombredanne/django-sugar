class CORSMiddleware(object):
    """
    Middleware that serves up JSON media types with a CORS header to 
    allow people to use your JSON data from JavaScript without requiring 
    them to proxy it.
    See: http://www.w3.org/TR/cors/

    Implement
    ---------
    Add to your middleware:

    'sugar.middleware.cors.CORSMiddleware',

    """

    def __init__(self):
        # should any others be added here?
        self.json_mediatypes = ["application/json", 
                                "application/x-suggestions+json",]

    def process_response(self, request, response):
        # just get the mediatype (strip charset)
        mediatype = response.get('content-type', '').split(";")[0].lower()
        if mediatype in self.json_mediatypes:
            response['Access-Control-Allow-Origin'] = '*'
        return response
