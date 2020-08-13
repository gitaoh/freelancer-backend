class AccessControlAllowOrigin:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Accept'] = 'application/json'
        response['X-Robots-Tag'] = 'none, noarchive'
        response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept'
        return response
