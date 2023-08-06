import json

import requests

from .core import ApiClient, BaseClient, who_am_i, JelasticClientException


class JpsClient(BaseClient):
    jelastic_group = "marketplace"

    jelastic_class = "jps"

    def __init__(self, api_client: ApiClient):
        super().__init__(api_client)

    def install_from_file(self, filename: str, env_name: str = None, settings: dict = None) -> str:
        try:
            file = open(filename, 'r')
        except OSError:
            raise JelasticClientException(f"Unable to open file {filename}")

        with file:
            manifest_content = file.read()
            return self.install(manifest_content, env_name, settings)

    def install_from_url(self, url: str, env_name: str = None, settings: dict = None) -> str:
        response = requests.get(url)
        if response.status_code != 200:
            raise JelasticClientException(f"Url not found: {url}")
        manifest_content = response.text
        return self.install(manifest_content, env_name, settings)

    def install(self, manifest_content: str, env_name: str = None, settings: dict = None) -> str:
        response = self._execute(
            who_am_i(),
            jps=manifest_content,
            envName=env_name,
            skipNodeEmails=True,
            settings=json.dumps(settings)
        )

        return response["successText"]

    def get_engine_version(self) -> str:
        response = self._execute(
            who_am_i()
        )

        return response["version"]
