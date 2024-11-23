from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Use a strong secret key from environment variables
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set in the environment variables!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))  # Default to 15 minutes if not set

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Password-related utility functions
def hash_password(password: str) -> str:
    """
    Hashes the given password using bcrypt.
    :param password: Plain text password to hash.
    :return: Hashed password as a string.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies the plain password against the hashed password.
    :param plain_password: The plain text password to verify.
    :param hashed_password: The hashed password for comparison.
    :return: True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


# JWT-related utility functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token.
    :param data: The data to include in the token payload.
    :param expires_delta: Optional expiration time for the token.
    :return: Encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decodes a JWT access token.
    :param token: The token to decode.
    :return: The decoded data as a dictionary.
    :raises HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTClaimsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Additional utilities for token creation and validation
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a refresh token with a longer expiration period.
    :param data: The data to include in the token payload.
    :param expires_delta: Optional expiration time for the token.
    :return: Encoded refresh token as a string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))  # Default 7 days for refresh token
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_token_and_extract_claims(token: str) -> dict:
    """
    Validates the JWT and extracts claims.
    :param token: The JWT token to validate.
    :return: Decoded claims from the token.
    :raises HTTPException: If the token is invalid or expired.
    """
    claims = decode_access_token(token)
    # Perform additional custom validations if needed
    return claims
