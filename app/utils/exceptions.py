from fastapi import HTTPException, status

class UserAlreadyExists(HTTPException):
    def __init__(self, field: str):
        detail = f"{field.capitalize()} already registered"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class CredentialsInvalid(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

class NotAuthenticated(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
