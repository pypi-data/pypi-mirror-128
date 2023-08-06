import requests
import os
from urllib.parse import urljoin

from i2a_oauth2_api_client.exceptions import I2AOauth2ClientException, I2AOauth2ClientUnauthorizedException,\
    I2AOauth2ClientValidationError, I2AOauth2ClientNotFoundError
from i2a_oauth2_api_client.enums import Environment


class I2AOauth2Client:

    I2A_OAUTH2_API_QA_SERVER_URL = 'https://oauth2-qa.i2asolutions.com'
    I2A_OAUTH2_API_PROD_SERVER_URL = 'https://oauth2.i2asolutions.com'
    I2A_OAUTH2_API_ROOT_PATH = '/api/v1'

    def __init__(self, client_id, client_secret, environment=Environment.QA):
        assert isinstance(environment, Environment)
        if environment is Environment.QA:
            self.url = self.I2A_OAUTH2_API_QA_SERVER_URL
        elif environment is Environment.PROD:
            self.url = self.I2A_OAUTH2_API_PROD_SERVER_URL
        else:
            raise NotImplementedError

        self.client_id = client_id
        self.client_secret = client_secret

    def ping(self):
        url = self._get_full_url('ping/')
        response = requests.get(url, headers=self._get_common_headers())
        if response.status_code != 200:
            raise I2AOauth2ClientException(
                f'Ping attempt at {url} has failed. Make sure I2A Oauth2 URL is correct and that the '
                f'service is running'
            )

    def register_user(self, email, password1, password2, first_name=None, last_name=None):
        full_username = self._build_full_username(email)
        return self.register_user_with_full_username(full_username, password1, password2, first_name, last_name)

    def register_user_with_full_username(self, username, password1, password2, first_name=None, last_name=None):
        data = {
            "username": username,
            "password1": password1,
            "password2": password2,
            "client_id": self.client_id
        }
        if first_name is not None:
            data['first_name'] = first_name
        if last_name is not None:
            data['last_name'] = last_name

        url = self._get_full_url('register/')
        response = requests.post(url, json=data, headers=self._get_common_headers())
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 400:
            raise I2AOauth2ClientValidationError(data=response.json())
        else:
            raise I2AOauth2ClientException(
                f'Create user failed. I2A Oauth API returned HTTP {response.status_code}.'
                f' Response text: {response.text}'
            )

    def get_token_with_full_username(self, username, password):
        url = self._get_full_url('auth/token/')
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "password",
            "username": username,
            "password": password
        }
        response = requests.post(url, data, headers=self._get_common_headers())
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise I2AOauth2ClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AOauth2ClientUnauthorizedException(data=response.json())
        else:
            raise I2AOauth2ClientException(
                f'Get token operation failed.'
                f' Authentication service returned HTTP {response.status_code}. Response text: {response.text}'
            )

    def get_token(self, email, password):
        full_username = self._build_full_username(email)
        return self.get_token_with_full_username(full_username, password)

    def check_token(self, token):
        url = self._get_full_url('me/')
        headers = self._get_common_headers()
        headers.update({
            "Authorization": f"Bearer {token}"
        })
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise I2AOauth2ClientUnauthorizedException(data=response.json())
        else:
            raise I2AOauth2ClientException(
                f'Check token operation failed.'
                f' Authentication service returned HTTP {response.status_code}. Response text: {response.text}'
            )

    def convert_token(self, backend, access_token):
        url = self._get_full_url('auth/convert-token/')
        headers = self._get_common_headers()
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "convert_token",
            "backend": backend,
            "token": access_token
        }
        response = requests.post(url, data, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise I2AOauth2ClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AOauth2ClientUnauthorizedException(data=response.json())
        else:
            raise I2AOauth2ClientException(
                f'Convert token operation failed.'
                f' Authentication service returned HTTP {response.status_code}. Response text: {response.text}'
            )

    def password_reset_request(self, email):
        url = self._get_full_url('server-to-server/password-reset-request/')
        headers = self._get_common_headers_with_secret()
        json = {
            "username": self._build_full_username(email)
        }
        response = requests.post(url, json=json, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            data = response.json()
            if data.get('error_information'):
                raise I2AOauth2ClientValidationError(data={'detail': data.get('error_information')})
            raise I2AOauth2ClientValidationError(data=data)
        elif response.status_code == 401:
            raise I2AOauth2ClientUnauthorizedException(data=response.json())
        else:
            raise I2AOauth2ClientException(
                f'Password reset request operation failed.'
                f' Authentication service returned HTTP {response.status_code}. Response text: {response.text}'
            )

    def password_reset(self, code, new_password1, new_password2):
        url = self._get_full_url('server-to-server/password-reset/')
        headers = self._get_common_headers_with_secret()
        json = {
            "code": str(code),
            "new_password1": new_password1,
            "new_password2": new_password2
        }
        response = requests.post(url, json=json, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise I2AOauth2ClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AOauth2ClientUnauthorizedException(data=response.json())
        else:
            raise I2AOauth2ClientException(
                f'Password reset operation failed.'
                f' Authentication service returned HTTP {response.status_code}. Response text: {response.text}'
            )

    def password_reset_code_check(self, code):
        url = self._get_full_url('server-to-server/password-reset-code-check/')
        headers = self._get_common_headers_with_secret()
        json = {
            "code": str(code),
        }
        response = requests.post(url, json=json, headers=headers)
        if response.status_code == 204:
            return None
        elif response.status_code == 400:
            raise I2AOauth2ClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AOauth2ClientUnauthorizedException(data=response.json())
        else:
            raise I2AOauth2ClientException(
                f'Password reset code check operation failed.'
                f' Authentication service returned HTTP {response.status_code}. Response text: {response.text}'
            )

    def password_change(self, token, old_password, new_password1, new_password2):
        url = self._get_full_url('password-change/')
        headers = self._get_common_headers()
        headers.update({
            "Authorization": f"Bearer {token}"
        })
        json = {
            "old_password": old_password,
            "new_password1": new_password1,
            "new_password2": new_password2
        }
        response = requests.post(url, json=json, headers=headers)
        if response.status_code == 200:
            return None
        elif response.status_code == 400:
            raise I2AOauth2ClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AOauth2ClientUnauthorizedException(data=response.json())
        else:
            raise I2AOauth2ClientException(
                f'Password change operation failed.'
                f' Authentication service returned HTTP {response.status_code}. Response text: {response.text}'
            )

    def delete_account(self, token):
        url = self._get_full_url('delete-account/')
        headers = self._get_common_headers()
        headers.update({
            "Authorization": f"Bearer {token}"
        })
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return None
        elif response.status_code == 400:
            raise I2AOauth2ClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AOauth2ClientUnauthorizedException(data=response.json())
        elif response.status_code == 404:
            raise I2AOauth2ClientNotFoundError(data=response.json())
        else:
            raise I2AOauth2ClientException(
                f'Delete account operation failed.'
                f' Authentication service returned HTTP {response.status_code}. Response text: {response.text}'
            )

    def delete_account_server_to_server(self, i2a_identifier):
        url = self._get_full_url(f'server-to-server/delete-account/{i2a_identifier}/')
        headers = self._get_common_headers_with_secret()
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return None
        elif response.status_code == 400:
            raise I2AOauth2ClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AOauth2ClientUnauthorizedException(data=response.json())
        elif response.status_code == 404:
            raise I2AOauth2ClientNotFoundError(data=response.json())
        else:
            raise I2AOauth2ClientException(
                f'Delete account server to server operation failed.'
                f' Authentication service returned HTTP {response.status_code}. Response text: {response.text}'
            )

    def _get_common_headers(self):
        return {
            'Client-Id': self.client_id
        }

    def _get_common_headers_with_secret(self):
        headers = self._get_common_headers()
        headers['Client-Secret'] = self.client_secret
        return headers

    def _get_full_url(self, resource_path):
        return urljoin(self.url, os.path.join(self.I2A_OAUTH2_API_ROOT_PATH, resource_path))

    def _build_full_username(self, email):
        return f"{email}@{self.client_id}"
