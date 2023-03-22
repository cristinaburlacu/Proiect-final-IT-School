import json

def get_success_response():
    return get_response({'success':True}, 200)

def get_error_response(value, code):
    return get_response({"error": value}, code)

def get_response(value, code):
    return json.dumps(value), code, {'ContentType': 'application/json'}