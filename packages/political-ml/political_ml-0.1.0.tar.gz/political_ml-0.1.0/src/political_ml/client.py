import logging
import uuid
from os.path import join

import requests

from political_ml.__meta__ import __version__
from political_ml.utils import check_payload_format, to_json

logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, endpoint, token):
        self._endpoint = endpoint
        self._token = token

    def exec_request(self, method, url, **kwargs):
        """ Executes a request, assigning a unique id beforehand and throwing on 4xx / 5xx """
        reqid = str(uuid.uuid4())

        logging.debug(
            f"{self.__class__.__qualname__} -> {method.upper()} {url} {reqid=}"
        )

        # requests.post / requests.get / ...
        method_exec = getattr(
            requests, method.lower()
        )  # retrieves the right method from requests

        headers = self._build_headers()
        response = method_exec(url, headers=headers, **kwargs)

        status_code = response.status_code
        content_length = len(response.content or "")
        logging.debug(
            f"{self.__class__.__qualname__} <- {status_code} {content_length} {reqid=}"
        )

        if response.status_code >= 300:
            logging.debug(response.json())

        # raise by default to halt further exec and bubble
        response.raise_for_status()

        return to_json(response)

    def build_url(self, *paths):
        return join(self._endpoint, *paths)

    def _build_headers(self):
        return {
            "Accept": "application/json",
            "User-Agent": f"Political ML Python package {__version__}",
            "Authorization": f"Bearer {self._token}",
        }

    def ner(self, payload) -> list:
        check_payload_format(payload)
        response = self.exec_request(
            method="POST",
            url=self.build_url("api/v1/ner"),
            json=payload,
        )
        return response or []

    def categorise(self, payload) -> list:
        check_payload_format(payload)
        response = self.exec_request(
            method="POST",
            url=self.build_url("api/v1/categorise"),
            json=payload,
        )
        return response or []
