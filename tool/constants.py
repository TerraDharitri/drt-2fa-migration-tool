import hashlib
from enum import Enum

IMAGES_EXTENSIONS = [".png", ".jpg", ".jpeg"]
URL_SCHEME_GOOGLE_OTPAUTH_MIGRATION = "otpauth-migration"
URL_SCHEME_OTP_AUTH = "otpauth"
DEFAULT_ALGORITHM_NAME = "sha1"
DEFAULT_ALGORITHM = hashlib.sha1
DEFAULT_NUM_DIGITS = 6
DEFAULT_INTERVAL = 30


class AuthAlgorithm(str, Enum):
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"
    MD5 = "md5"
