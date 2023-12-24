from django.http import HttpResponse
import json
from rest_framework.views import exception_handler

class CustomResponse(HttpResponse):
    def __init__(self, data=None, statuscode=None, message=None, issuccess=True, content_type='application/json'):
        response_data = {
            'statuscode': statuscode,
            'message': message or self.get_default_message(statuscode),
            'issuccess': issuccess,
            'data': data,
        }
        response_json = json.dumps(response_data)

        super().__init__(content=response_json, content_type=content_type)

    def get_default_message(self, status):
        status_messages = {
            200: "Success",
            201: "Created",
            204: "Deleted",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Access Forbidden",
            404: "Not Found",
            415: "Unsupported File Type",
            413: "Request entity too large",

        }
        
        return status_messages.get(status, "Unknown Status")

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    error = {
        'msg':f'{exc}'
    }
    if response is not None:
        response = CustomResponse(None, response.status_code, f'{error["msg"]}' ,False)
    
    return response
