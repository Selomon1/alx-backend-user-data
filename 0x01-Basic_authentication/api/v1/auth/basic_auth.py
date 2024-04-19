#!/usr/bin/env python3

from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """ class BasicAuth """

    def extract_base64_authorization-header(self, authorization_header: str) -> str:
        """ Extracts the Base64 part of the Authorization header for
        Basic Authorization
        """
        if authorization_header is None or \
           not isinstance(authorization_header, str) or \
           not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Decodes the base64 authorization header """
        if base64_authorization_header is None or \
           not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_header = base64.b64decode(base64_authorization_header)
            return decoded_header.decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts user email and pwd from the decoded base64 authorization
        header
        """
        if (decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str) or
            ':' not in decoded_base64_authorization_header:
            return None, None
        return decoded_base64_authorization_header.split(':', 1)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Retrieves the user instanse based on email and pwd """
        if user_email is None or not isinstance(user_email, str) or \
                user_pwd is None or not isinstance(user_pwd, pwd):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid-password(user_pwd):
            return none
        return user

    def current_user(self, request=None) -> Typevar('User'):
        """ overloads Auth's current_user method """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None or \
           not isinstance(auth_header, str) or \
           not auth_header.startswith('Basic '):
            return None
        base64_part = self.extract_base64_authorization_header(auth_header)
        decoded_part = self.decode_base64_authorization_header(base64_part)
        email, pwd = self.extract_user_credentials(decoded_part)
        return self.user_object_from_credentials(email, pwd)
