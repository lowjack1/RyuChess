import functools
from datetime import datetime, timedelta
from hashlib import sha256
from uuid import uuid4
import urllib.parse
from urllib.parse import urlencode

import aiohttp
import bleach
from tornado.ioloop import IOLoop
from tornado.web import HTTPError, RequestHandler


class BaseHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        '''
        Over-riding default function to save the logs on error
        Docs: https://www.tornadoweb.org/en/stable/_modules/tornado/web.html#RequestHandler.write_error
        '''
        if "exc_info" in kwargs:
            requestHandlerErrorLogging(self, kwargs["exc_info"])
        
        self.finish(
            "<html><title>%(code)d: %(message)s</title>"
            "<body>%(code)d: %(message)s</body></html>"
            % {"code": status_code, "message": self._reason}
        )

    def write_api_response(self, data, status=True, msg="", code=None):
        '''
        Function to generate a standard response for API calls

        Function parameters:
            • data      : Data to be passed to the client
            • status    : Gives high level idea of request. Can have two possible values: True / False
            • msg       : Optional message

        Response parameters:
            • status    : Same idea of function parameter. Client should only start processing, if status is True
            • code      : If status is bad, code allows for more specific tagging of error type
                            > Currently it cannot be set explicitly by parent API handlers, because the requirements are not well chalked out.
                              At this point, it can have 2 values 200 / 400
                              So exists by design, but not exploited to full potential.
            • msg       : For human response that can be shown as alerts on client device
            • result    : Contains the data for the API call.
                          As per current design, it will have following keys:
                            > user
                            > data

        Rules:
            1. `user` key in `result` will be None, for non-logged in users
            2. `result` key will be None, if status is not True. In that case no data will be forwarded to client even though it is passed to this function
        '''
        status = True if status == True else False      # This is just to ensure that "status" flag nature is explicitly decided by Boolean and not by implicit type-casting
        if code is None:                                # If the code is not set explicitly, then switch between 200 & 400 based on status
            code = 200 if status else 400
        resp = {
            "status": status,
            "code": code,
            "msg": msg,
            "result": {'user': None, 'data': data} if status else None
        }
        # Update user data if logged in
        if status and self.current_user:
            resp['result']['user'] = {
                "name": self.current_user_name,
                "level": self.access_level
            }
        self.write(resp)
