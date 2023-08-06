import requests


class SabyVokClient:
    _host = 'http://api.sbis.ru/vok/'
    _oauth_url = 'https://api.sbis.ru/oauth/service/'

    def __init__(self, client_id, secret, key):
        """
        Args:
            client_id (str): client id
            secret (str): client secret
            key (str): client service key
        """
        self._client_id = client_id
        self._secret = secret
        self._key = key
        self._session_id = None
        self._access_token = None

    def req(self, inn=None, ogrn=None):
        """
        Main requisites

        Args:
            inn (str): INN
            ogrn (str): OGRN

        Returns:
            dict: https://github.com/saby/vok/blob/main/doc/req/README.md
        """
        return self._perform_request(
            'req',
            {
                'inn': inn,
                'ogrn': ogrn,
            }
        )

    @property
    def _request_headers(self):
        """
        Request headers with auth data

        Returns:
            dict: request headers
        """
        return {
            "User-Agent": "SabyVok Python Client / 1.0.0",
            "X-SBISAccessToken": self._saby_access_token,
            "X-SBISSessionId": self._saby_session_id,
            "Content-Type": "application/json; charset=utf-8",
        }

    @property
    def _saby_session_id(self):
        """
        Session id for request

        Returns:
            str: Saby session id
        """
        if self._session_id is None:
            self._obtain_saby_session()
        return self._session_id

    @property
    def _saby_access_token(self):
        """
        Access token for request

        Returns:
            str: Saby access token
        """
        if self._access_token is None:
            self._obtain_saby_session()
        return self._access_token

    def _obtain_saby_session(self):
        """
        Obtain session id from Saby
        """
        response = requests.post(
            self._oauth_url,
            json={
                "app_client_id": self._client_id,
                "app_secret": self._secret,
                "secret_key": self._key,
            }
        ).json()
        self._access_token = response['access_token']
        self._session_id = response['sid']

    def _perform_request(self, url, params):
        """
        Performs the request to Saby API

        Args:
            url (str): url
            params (dict): get params

        Returns:
            dict: obtained data
        """
        full_url = f'{self._host}{url}'
        return requests.get(full_url, params, headers=self._request_headers).json()
