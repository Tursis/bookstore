from jwcrypto import jwt, jwk


class AccountToken:
    def create_token(self):
        token = jwk.JWK(generate='oct', size=256)

        return token.export()
