import logging
import typing
import uuid
from os.path import join

import requests

from source_aggregation.__meta__ import __version__
from source_aggregation.utils import to_json


logger = logging.getLogger(__name__)
ArtifactId = typing.Union[int, str]


class _BaseClient:
    """
    Client that exposes required source aggregation service endpoints

    Adds logging and tracing of requests and responses in debug mode. Raises on errors during request.
    """

    def __init__(self, endpoint, token):
        self._endpoint = endpoint
        self._token = token

    def exec_request(self, method: str, url: str, **kwargs):
        """Executes a request, assigning a unique id beforehand and throwing on 4xx / 5xx"""
        reqid = str(uuid.uuid4())

        logger.debug(
            f"{self.__class__.__qualname__} -> {method.upper()} {url} {reqid=}"
        )

        # requests.post / requests.get / ...
        method_exec = getattr(requests, method.lower())

        headers = self._build_headers()
        response = method_exec(url, headers=headers, **kwargs)

        status_code = response.status_code
        content_length = len(response.content or "")
        logger.debug(
            f"{self.__class__.__qualname__} <- {status_code} {content_length} {reqid=}"
        )

        # raise by default to halt further exec and bubble
        response.raise_for_status()

        return to_json(response)

    def build_url(self, *paths):
        return join(self._endpoint, *paths)

    def _build_headers(self):
        return {
            "Accept": "application/json",
            "User-Agent": f"SAS Python package {__version__}",
            "Authorization": f"Bearer {self._token}",
        }


class Sources(_BaseClient):
    def list(self, params: dict = None) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url("source"),
            params=(params or {}),
        )
        return response or {}

    def get(self, source_id: str) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url(f"source/{source_id}"),
        )
        return response or {}

    def create(self, source_kwargs: dict) -> dict:
        response = self.exec_request(
            method="POST", url=self.build_url("source"), json=source_kwargs
        )
        return response or {}

    def update(self, source_id: str, source_kwargs: dict) -> dict:
        response = self.exec_request(
            method="PUT", url=self.build_url(f"source/{source_id}"), json=source_kwargs
        )
        return response or {}


class SourceLogs(_BaseClient):
    def create(self, source_id: str, log_kwargs: dict) -> dict:
        response = self.exec_request(
            method="POST",
            url=self.build_url("source", source_id, "history"),
            json=log_kwargs,
        )
        return response or {}

    def list(self, source_id: str, params: dict = None) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url("source", source_id, "logs"),
            params=(params or {}),
        )
        return response or {}


class SourceHistory(_BaseClient):
    def list(self, source_id: str, params: dict = None) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url("source", source_id, "history"),
            params=(params or {})
        )
        return response or {}


class Artifacts(_BaseClient):
    def list(self, params: dict = None) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url("artifact"),
            params=(params or {}),
        )
        return response or {}

    def get(self, artifact_id: str) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url(f"artifact/{artifact_id}"),
        )
        return response or {}

    def create(self, source_id: str, artifact_kwargs: dict) -> dict:
        response = self.exec_request(
            method="POST",
            url=self.build_url(f"source/{source_id}/artifact"),
            json=artifact_kwargs,
        )
        return response or {}

    def update(self, artifact_id: str, artifact_kwargs: dict) -> dict:
        response = self.exec_request(
            method="PUT",
            url=self.build_url(f"artifact/{artifact_id}"),
            json=artifact_kwargs,
        )
        return response or {}

    def export(self, artifacts) -> list:
        ids = ",".join(str(artifact.get("id")) for artifact in artifacts)
        response = self.exec_request(
            method="POST",
            url=self.build_url(f"artifact/{ids}/export"),
        )
        return response.get("id") or []

    def ignore(self, artifacts) -> list:
        ids = ",".join(str(artifact.get("id")) for artifact in artifacts)
        response = self.exec_request(
            method="POST",
            url=self.build_url(f"artifact/{ids}/ignore"),
        )
        return response.get("id") or []


class Labels(_BaseClient):
    def list(self, params: dict = None) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url("label"),
            params=(params or {}),
        )
        return response or {}

    def get(self, label_id: str) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url(f"label/{label_id}"),
        )
        return response or {}

    def create(self, label_kwargs: dict) -> dict:
        response = self.exec_request(
            method="POST", url=self.build_url("label"), json=label_kwargs
        )
        return response or {}

    def update(self, label_id: str, label_kwargs: dict) -> dict:
        response = self.exec_request(
            method="PUT", url=self.build_url(f"label/{label_id}"), json=label_kwargs
        )
        return response or {}

    def delete(self, label_id: str) -> dict:
        response = self.exec_request(
            method="DELETE", url=self.build_url(f"label/{label_id}")
        )
        return response or {}


class Categories(_BaseClient):
    def list(self, params: dict = None) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url("category"),
            params=(params or {}),
        )
        return response or {}

    def get(self, category_id: str) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url(f"category/{category_id}"),
        )
        return response or {}

    def create(self, category_kwargs: dict) -> dict:
        response = self.exec_request(
            method="POST", url=self.build_url("category"), json=category_kwargs
        )
        return response or {}

    def update(self, category_id: str, category_kwargs: dict) -> dict:
        response = self.exec_request(
            method="PUT",
            url=self.build_url(f"category/{category_id}"),
            json=category_kwargs,
        )
        return response or {}

    def delete(self, category_id: str) -> dict:
        response = self.exec_request(
            method="DELETE", url=self.build_url(f"category/{category_id}")
        )
        return response or {}

    def preview(self, preview_kwargs):
        response = self.exec_request(
            method="POST",
            url=self.build_url("category/preview"),
            json=preview_kwargs,
        )
        return response or {}

    def infer(self, infer_kwargs):
        response = self.exec_request(
            method="POST",
            url=self.build_url("category/infer"),
            json=infer_kwargs,
        )
        return response or {}


class ApiClient:
    artifacts: Artifacts
    sources: Sources
    source_logs: SourceLogs
    source_history: SourceHistory
    categories: Categories
    labels: Labels

    def __init__(self, endpoint, token):
        self._endpoint = endpoint
        self._token = token

    def __getattr__(self, name):
        """Method that automatically resolves the type"""
        annot_type = self.__class__.__annotations__.get(name)
        if annot_type and issubclass(annot_type, _BaseClient):
            return self._build_client(annot_type)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has attribute '{name}'"
        )

    def _build_client(self, client_type):
        return client_type(self._endpoint, self._token)
