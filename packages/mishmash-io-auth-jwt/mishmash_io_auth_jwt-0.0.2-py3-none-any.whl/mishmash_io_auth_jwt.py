# Copyright 2019 MISHMASH I O OOD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
import time
import traceback

import jwt
import requests
from Crypto.PublicKey import RSA


class MishmashAuthUnauthorizedException(Exception):
    pass

class MishmashAuthInvalidRsaKey(Exception):
    pass

class MishmashAuthInvlaidRequestForAccessToken(Exception):
    pass

class MishmashAuth():

    
    SIGNED_TOKEN_VALID_TIME = 3600

    def __init__(self, server_address_list, config_data):

        self.__auth_app_id = config_data["MISHMASHIO_APP_ID"]
        self.__auth_server_url = config_data["MISHMASHIO_AUTH_SERVER"]
        self.__auth_server_url_token = config_data["MISHMASHIO_AUTH_SERVER"] + "/protocol/openid-connect/token"
        self.__auth_private_key_string = config_data["MISHMASHIO_AUTH_PRIVATE_KEY"]
        self.__server_address_list = server_address_list
        self.__access_token = None

    @staticmethod
    def __has_rsa_headers(key):
        """
            Check if provided rsa key has rsa headers

            Returns:
                bool: return True if provided key has rsa headers 
                    False otherwise
        """

        if '-----BEGIN RSA PRIVATE KEY-----\n' in key:
            if '\n-----END RSA PRIVATE KEY-----' in key:
                return True
            else:
                raise MishmashAuthInvalidRsaKey(
                    "Invalid rsa header - no end header, check your key ")
        return False

    def __add_rsa_headers_to_private_key(self, key_without_pem_headers):
        """
            Add rsa headers to private key if there not

            Returns:
                string: return fixed rsa headers 
        """

        if MishmashAuth.__has_rsa_headers(key_without_pem_headers):
            return key_without_pem_headers

        pem_key = "-----BEGIN RSA PRIVATE KEY-----\n"
        pem_key += key_without_pem_headers
        pem_key += "\n-----END RSA PRIVATE KEY-----"
        return pem_key

    def has_token_expired(self, token):
        """
            Checks if jwt token has been expired

            Returns:
                bool: return True if access token has been expired
                    False otherwise
        """
        decoded_token = jwt.decode(token, audience=self.__auth_server_url, options={
                           "verify_signature": False, 'verify_aud': False})
        
        if time.time() - decoded_token["exp"] >= 0:
            return True

        return False

    def __sign_client_token(self):
        """
            Returns signed jwt with the private key

            Returns:
                str: jwt formated signed token with private key
        """
        iat = time.time()
        exp = iat + self.SIGNED_TOKEN_VALID_TIME
        payload = {
            "exp": exp,
            "iat": iat,
            "iss": self.__auth_app_id,
            "sub": self.__auth_app_id,
            "aud": self.__auth_server_url,
            "jti": str(uuid.uuid4()),
            "uid": self.__auth_app_id,
            "scope": self.__server_address_list
        }

        private_key = RSA.importKey(
            self.__add_rsa_headers_to_private_key(self.__auth_private_key_string))

        return jwt.encode(payload,
                          private_key.exportKey('PEM'),
                          algorithm='RS256')

    def __generate_new_access_token(self):
        """ Generate new oidc access token from request to 
            authentication server 

            Returns:
                    str: generated new access token  
        """

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            "client_id": self.__auth_app_id,
            "scope": "openid",
            "grant_type": "client_credentials",
            "client_assertion_type": 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            "client_assertion": self.__sign_client_token()
        }

        try:
            response = requests.post(self.__auth_server_url_token,
                                     data=data, headers=headers).json()
        except Exception as e:
            raise MishmashAuthInvlaidRequestForAccessToken(traceback.print_tb(e.__traceback__, e.args))
            
        if "error" in response:
            raise MishmashAuthUnauthorizedException(f"{response}")
        else:
            return response.get("access_token", None)

    def __get_or_create_access_token(self):
        """
           Returns cached access token if it has been generated and 
           has not been expired or creates new one 

           Returns:
                str: generated or cached access token  
        """

        if self.__access_token is None:
            self.__access_token = self.__generate_new_access_token()

        if self.has_token_expired(self.__access_token):
            self.__access_token = self.__generate_new_access_token()

        return self.__access_token

    @property
    def app_id(self):
        """ Returns mishmash app id which represent the issuer 
            of the grpc call

            Returns:
                str: issuer of the grpc call
        """
        return self.__auth_app_id

    @property
    def access_token(self):
        """ Create new or use cached access token to generate 
            new authorization token for mishmash grpc call

            Returns:
                str: generated or cached access token  
        """

        authorization_token = self.__get_or_create_access_token()

        if not authorization_token:
            raise MishmashAuthUnauthorizedException(
                "Invalid access token token, Please, check your credentials")

        return authorization_token

    @property
    def authorization_header(self):
        """ Create new or use cached access token to generate 
            new authorization header string for mishmash grpc call

            Returns:
                str: string with format 'Bearer access_token'
        """
        return f"Bearer {self.access_token}"
