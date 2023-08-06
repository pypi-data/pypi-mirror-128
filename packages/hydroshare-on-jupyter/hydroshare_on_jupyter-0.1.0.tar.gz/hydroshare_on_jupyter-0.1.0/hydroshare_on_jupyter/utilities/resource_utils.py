from pydantic import BaseModel, Field
from typing import Dict, List
from pathlib import Path
import re
import requests


class RemoteResource(BaseModel):
    file_name: str = Field(...)
    checksum: str = Field(...)


class RemoteResourceList(BaseModel):
    __root__: List[RemoteResource]


class Resource:
    _MANIFEST_MD5_RE = re.compile(r"(^\w+)[\s]*(data/contents.*$)", re.M)

    def __init__(self, session: requests.Session):
        self._session = session
        self._resources = dict()

    def list_files(self, resource_id: str) -> List[RemoteResource]:
        if resource_id not in self._resources:
            self._build_file_list(resource_id)

        return self._resources[resource_id]

    def refresh(self, resource_id: str):
        if resource_id not in self._resources:
            return

    def _get_manifest_md5(self, resource_id: str):
        url = f"https://www.hydroshare.org/resource/{resource_id}/manifest-md5.txt"
        res = requests.get(url)
        return res.text

    def _build_file_list(self, resource_id: str):
        res = self._get_manifest_md5(resource_id)
        parsed_results = self._parse_file_list(res)
        self._resources[resource_id] = parsed_results

    def _parse_file_list(self, manifest_text: str) -> Dict[Path, str]:
        results = self._MANIFEST_MD5_RE.finditer(manifest_text)

        resources = {}
        for r in results:
            checksum, file_name = r.groups()
            resources[Path(file_name)] = checksum

        return resources
