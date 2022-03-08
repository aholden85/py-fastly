#!/usr/bin/python3

import base64
import urllib.parse
import json
import requests


class FastlySession(requests.Session):
    def __init__(self, *args, **kwargs):
        super(FastlySession, self).__init__(*args, **kwargs)

    def init_basic_auth(self, access_token):
        self.headers.update(
            {
                "Accept": "application/json",
                "Fastly-Key": access_token
                # 'User-Agent': 'Python-ClientLibrary'
            }
        )


class FastlyClient(object):
    def __init__(self, access_token):
        """
        Instantiate a new API client.
        Args:
            access_token (str): RPC access token for protected APIs.
        """
        # Initialize the session.
        self.__session = FastlySession()

        # Pass the authentication credentials to the session.
        self.__session.init_basic_auth(access_token)

        self.__endpoint = "https://api.fastly.com"

    def __request(self, method, path, params=None, data=None, headers={}):
        # There are a specific set of methods that can be executed.
        valid_methods = [
            "GET",
            "OPTIONS",
            "HEAD",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        ]
        if method not in valid_methods:
            raise ValueError(
                "FastlyClient.__request: method must be one of {0}.".format(
                    valid_methods
                )
            )

        req = requests.Request(
            method=method,
            url="{}/{}".format(
                self.__endpoint,
                path,
            ),
            params=params,
            data=data,
            headers=headers,
        )

        if data is not None:
            req.headers["Content-Type"] = "application/json"

        prep = self.__session.prepare_request(req)
        resp = self.__session.send(prep)
        return resp

    def list_services(self):
        path = "services"

        return self.__request(
            method="GET",
            path=path,
        )

    def list_service_domains(self, service_id):
        path = "service/{}/domain".format(
            service_id,
        )

        return self.__request(
            method="GET",
            path=path,
        )