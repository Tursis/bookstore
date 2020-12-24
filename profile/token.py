from jwcrypto import jwt, jwk
from .models import Token


class AccountToken:
    """
    Создание токена регистрации
    """
    def create_token(self, user):
        key = jwk.JWK(generate='oct', size=256)
        token = jwt.JWT(header={"alg": "HS256"},
                        claims={"info": user})
        token.make_signed_token(key)
        return token.serialize()
