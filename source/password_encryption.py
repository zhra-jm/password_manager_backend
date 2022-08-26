from passlib.context import CryptContext
import string
from random import choices


class Encryption:
    PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated="auto")

    def password_encryption(self, password):
        return self.PWD_CONTEXT.hash(password)

    def check_password(self, user_password, hashed_password):
        return self.PWD_CONTEXT.verify(user_password, hashed_password)

    @staticmethod
    def create_password(length=12, upper=True, lower=True, digit=True, pun=True):
        pool = ''

        if upper:
            pool += string.ascii_uppercase

        if lower:
            pool += string.ascii_lowercase

        if digit:
            pool += string.digits

        if pun:
            pool += string.punctuation

        if pool == '':
            pool = string.ascii_letters

        return ''.join(choices(pool, k=length))


encryption = Encryption()
