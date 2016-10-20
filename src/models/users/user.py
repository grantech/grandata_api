import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants
from src.models.alert.alert import Alert


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {} ".format(self.email)

    @staticmethod
    def is_login_valid(email, password):

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exists")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email, password):
        user_data = Database.find(UserConstants.COLLECTION, {"email": email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email does not have th right format")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION,self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return  cls(**Database.find_one(UserConstants.COLLECTION,{"email": email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)



