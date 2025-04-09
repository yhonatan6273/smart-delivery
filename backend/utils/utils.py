from passlib.context import CryptContext


pwt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash_password(password:str):
    return pwt_context.hash(password)