from kernel.database import BaseHelper, DB


class User(DB.Model):
    __tablename__ = 'users'

    id = DB.Column(DB.Integer(), nullable=False)
    name = DB.Column(DB.String(64), nullable=False, default='')


class UserHelper(BaseHelper):
    __model__ = User

    id = None
    name = None
