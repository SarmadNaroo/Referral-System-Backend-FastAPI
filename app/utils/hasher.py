import bcrypt

class Hasher:
    @staticmethod
    def hash_password(plain_text_password: str) -> str:
        """Hash a plaintext password."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_text_password.encode("utf-8"), salt)
        print("inside hash_password")
        print("plain_text_password", plain_text_password)
        print("hashed_password", hashed_password)
        return hashed_password.decode("utf-8") 

    @staticmethod
    def verify_password(plain_text_password: str, hashed_password: str) -> bool:
        """Verify a plaintext password against a hashed password."""
        return bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_password.encode("utf-8"))
