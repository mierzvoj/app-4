import json
from datetime import datetime

import jwt
import datetime
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response, JSONResponse
from jwt import ExpiredSignatureError
from commands import users_commands
from commands.users_commands import register, WrongDataException, UserExistsException, users_list
from database.database import get_database
from authorization import generate_jwt, decode_jwt
from json import JSONEncoder


class Login(HTTPEndpoint):
    async def post(self, request):
        body = await request.json()
        if 'login' not in body or 'password' not in body:
            return Response(JSONResponse({}).body, status_code=400)
        db = get_database()
        out = users_commands.login(db, body['login'], body['password'])
        if out is None:
            return Response(JSONResponse({}).body, status_code=401)
        expiry = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=15)
        token = jwt.encode({'exp': expiry, 'sub': out.id}, 'secret', algorithm='HS256')
        return JSONResponse({'token': token})


class Register(HTTPEndpoint):
    async def post(self, request):
        body = await request.json()

        if 'login' not in body or 'password' not in body:
            return Response(JSONResponse({"error": "wrong_data"}).body, status_code=400)

        try:
            register(get_database(), body['login'], body['password'])
        except WrongDataException:
            return Response(JSONResponse({"error": "wrong_data"}).body, status_code=400)
        except UserExistsException:
            return Response(JSONResponse({"error": "existing_user"}).body, status_code=400)

        return JSONResponse({})


class Refresh(HTTPEndpoint):
    async def post(self, request):
        if 'authorization' not in request.headers:
            return Response(JSONResponse({}).body, status_code=403)

        token: str = request.headers['authorization']
        if not token.startswith("JWT "):
            return Response(JSONResponse({}).body, status_code=403)
        token = token[4:]
        user_id = decode_jwt(token)
        print(user_id)
        if user_id is None:
            return Response(JSONResponse({}).body, status_code=403)
        return JSONResponse({token: generate_jwt(user_id)})


class List(HTTPEndpoint):
    async def get(self, request):
        if 'authorization' not in request.headers:
            return Response(JSONResponse({}).body, status_code=403)
        token: str = request.headers['authorization']
        if not token.startswith("JWT "):
            return Response(JSONResponse({}).body, status_code=403)
        users = (users_list(get_database()))
        # json_string = json.dumps([ob.__dict__ for ob in users])
        # return JSONResponse(json_string)
        return JSONResponse(json.dumps(users, default=lambda o: o.__dict__, sort_keys=True))
