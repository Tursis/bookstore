from jwcrypto import jwt, jwk


class AccountToken:
    def create_token(self, user):
        key = jwk.JWK(generate='oct', size=256)
        Token = jwt.JWT(header={"alg": "HS256"},
                        claims={"info": user})
        Token.make_signed_token(key)
        return Token.serialize()
