from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        print("inside verify_password")
        print("plain_password", plain_password)
        print("hashed_password", hashed_password)
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        print("inside get_password_hash")
        print("password", password)
        return pwd_context.hash(password)