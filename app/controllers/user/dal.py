from models import HELPERS


def get_user_by_id(*, id):
    UserHelper = HELPERS['User']
    User = UserHelper.get_model()
    user = User.query.get(id)
    if user:
        return UserHelper(user)
    else:
        return None


def get_user_by_name(*, name):
    UserHelper = HELPERS['User']
    User = UserHelper.get_model()
    user = User.query.filter_by(name=name).first()
    if user:
        return UserHelper(user)
    else:
        return None
