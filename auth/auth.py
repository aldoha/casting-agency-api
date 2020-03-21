import json
import os
from functools import wraps
from urllib.request import urlopen

from flask import _request_ctx_stack, request
from jose import jwt
from dotenv import load_dotenv


load_dotenv('.env')
domain = os.getenv('AUTH0_DOMAIN')
algorithms = os.getenv('ALGORITHMS')
audience = os.getenv('API_AUDIENCE')


class AuthError(Exception):

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    header = request.headers.get('Authorization')
    if not header:
        raise AuthError("Authorization header is expected", 401)

    auth_headers = header.split()

    if auth_headers[0].lower() != 'bearer':
        raise AuthError("Authorization header must start with 'Bearer'", 401)
    elif len(auth_headers) == 1:
        raise AuthError("Token not found", 401)
    elif len(auth_headers) > 2:
        raise AuthError("Authorization header must be Bearer token", 401)

    token = auth_headers[1]

    return token


def check_permissions(permission, payload):
    if payload['permissions'] is None:
        raise AuthError('No permissions found', 400)
    if permission not in payload['permissions']:
        raise AuthError('Access denied', 403)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{domain}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError('Authorization malformed', 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=algorithms,
                audience=audience,
                issuer='https://' + domain + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError('Token expired.', 401)

        except jwt.JWTClaimsError:
            raise AuthError(
                'Incorrect claims. Please, check the audience and issuer.',
                401
            )
        except Exception:
            raise AuthError('Unable to parse authentication token.', 400)
    raise AuthError('Unable to find the appropriate key.', 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
