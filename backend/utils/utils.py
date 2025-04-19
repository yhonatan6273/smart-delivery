from passlib.context import CryptContext


pwt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash_password(password:str):
    return pwt_context.hash(password)
#make the normal password to hashed password
def verify_password(plain_password,hashed_password):
    return pwt_context.verify(plain_password,hashed_password)