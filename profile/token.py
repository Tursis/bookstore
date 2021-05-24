from jwcrypto import jwt, jwk
from .models import Token


def create_token(user):
    """
    Создание токена регистрации
        """
    key = jwk.JWK(generate='oct', size=256)
    token = jwt.JWT(header={"alg": "HS256"},
                    claims={"info": user})
    token.make_signed_token(key)
    return token.serialize()
