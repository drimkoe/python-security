import token
import jwt
from flask import request, abort, current_app
from functools import wraps

user_ids = [{"user_id":"james"},{"user_id":"mike"},{"user_id":"john"},{"user_id":"admin"}]

def token_is_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "error":"Unauthorized",
                "message":"No authentication token",
                "data": None
            }, 401

        try:
            data = jwt.decode(token,current_app.config["SECRET_KEY"],algorithms=["HS256"])
            user_id = [u for u in user_ids if u["user_id"] == data["user_id"]]
            print(user_id)
            if user_id is None or len(user_id) == 0:
                  return {
                    "error":"Unauthorized",
                    "message":"Invalid authentication token",
                    "data": None
                }, 401
        except Exception as e:
                  return {
                    "error":"Unauthorized",
                    "message":str(e),
                    "data": None
                }, 500
        
        return f(user_id,*args,**kwargs)
    return decorated

