from database.users_model import User
from rooms import rooms_service
from users import users_service


class RegisterException(Exception):
    pass


class WrongDataException(RegisterException):
    pass


class UserExistsException(RegisterException):
    pass


def register(db, login, password):
    if not users_service.validate_login(login):
        raise WrongDataException("Wrong login")

    if not users_service.validate_password(password):
        raise WrongDataException("Wrong password")

    if users_service.has_user(db, login):
        raise UserExistsException("User exists")

    with db:
        users_service.create_user(db, login, password)


def login(db, login, password) -> User:
    print(User)
    return users_service.login(db, login, password)


def users_list(db):
    return users_service.get_all_users(db)


def rooms_list(db, id: int):
    return rooms_service.get_room(db, id)


def room_create(db, owner_id: int, password: str, name: str):
    return rooms_service.create_room(db, owner_id, password, name)


def room_join(db, id: int, room_id: int, password: str):
    return rooms_service.join_room(db, id, room_id, password)
