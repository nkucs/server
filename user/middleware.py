from django.contrib.sessions.models import Session
from django.utils.deprecation import MiddlewareMixin
from utils.api import JSONResponse
from user.models import User

class APISessionAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            session_id = request.COOKIES['sessionID']
            if session_id:
                try:
                    print('session_id:', session_id)
                    sess_dict = Session.objects.get(pk=session_id).get_decoded()
                    print(sess_dict)
                    user_id = sess_dict['user_id']
                    request.user = User.objects.get(id=user_id)
                except Exception:
                    #return JSONResponse.response({"error": "login-required", "data": "Please login in first"})
                    pass
        except:
            pass

