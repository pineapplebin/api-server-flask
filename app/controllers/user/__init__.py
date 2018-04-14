from ..controller import CustomController
from kernel.auth import current_user
from kernel.controller.webargs import fields
from kernel.response import Response, THolder

from app.backends import Backend
from .dal import get_user_by_name

user_controller = CustomController(
    name='user', import_name=__name__, prefix='/user')
_C = user_controller

login_response = {
    'token': THolder('token')
}

login_params = {
    'name': fields.Str(required=True),
}


@_C.post('/login')
@_C.use_args(login_params, code=401)
@_C.add_apidoc(response=login_response)
def login(parsed):
    user = get_user_by_name(name=parsed['name'])
    if not user:
        return Response.raw(code=401)

    token = Backend.encode({'user_id': user.id})
    return Response.render(login_response, token=token)


user_info_response = {
    'user': {
        'id': THolder('user.id'),
        'name': THolder('user.name')
    }
}


@_C.get('/user-info')
@_C.login_required()
@_C.add_apidoc(response=user_info_response)
def user_info():
    return Response.render(user_info_response, user=current_user)
