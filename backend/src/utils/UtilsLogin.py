from passlib.context import CryptContext

# Setting up password hashing context
pwt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

# Function to hash password
def hash_password(password:str):
    return pwt_context.hash(password)


# Function to verify password
# User will provide his password and then we will compare it with the hashed password stored in DB (by hashing the user provided password and comparing both hashes)
def verify_password(plain_password,hashed_password):
    return pwt_context.verify(plain_password,hashed_password)