from flask import request, abort

def request_is_authenticated(func):
    def wrapper(*args, **kwargs):

        key = args[0].get('api_key')
        request_key = request.args.get('api_key')

        if key:
            if request_key != key:
                abort(403)

        return func(*args, **kwargs)

    return wrapper