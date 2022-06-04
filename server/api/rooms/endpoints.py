import json
from datetime import datetime

import jwt
import datetime
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response, JSONResponse
from jwt import ExpiredSignatureError
from commands import users_commands
from commands.users_commands import register, WrongDataException, UserExistsException, users_list, rooms_list, \
    room_create, room_join
from database.database import get_database
from authorization import generate_jwt, decode_jwt
from json import JSONEncoder

from rooms.rooms_service import create_room


class List(HTTPEndpoint):
    async def get(self, request):
        if 'authorization' not in request.headers:
            return Response(JSONResponse({}).body, status_code=403)
        token: str = request.headers['authorization']
        if not token.startswith("JWT "):
            return Response(JSONResponse({}).body, status_code=403)
        token = token[4:]
        user_id = decode_jwt(token)
        list = (rooms_list(get_database(), user_id))
        return JSONResponse(json.dumps(list, default=lambda o: o.__dict__, sort_keys=True))


class Create(HTTPEndpoint):
    async def post(self, request):
        body = await request.json()
        if 'authorization' not in request.headers:
            return Response(JSONResponse({}).body, status_code=403)
        token: str = request.headers['authorization']
        if not token.startswith("JWT "):
            return Response(JSONResponse({}).body, status_code=403)
        token = token[4:]
        owner_id = decode_jwt(token)
        room_create(get_database(), body['owner_id'], body['name'], body['password'])
        return JSONResponse({})


class Join(HTTPEndpoint):
    async def post(self, request):
        body = await request.json()
        if 'authorization' not in request.headers:
            return Response(JSONResponse({}).body, status_code=403)
        token: str = request.headers['authorization']
        if not token.startswith("JWT "):
            return Response(JSONResponse({}).body, status_code=403)
        token = token[4:]
        user_id = decode_jwt(token)
        room_join(get_database(), user_id, request.path_params['id'], body["password"])
        return JSONResponse({})
