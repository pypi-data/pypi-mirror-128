import base64
from typing import Dict, List

from requests import Response

from ...core import CFDI
from . import utils
from .enums import RequestType
from .package_parsers import XML2CFDI, Metadata2CFDI
from .response_parsers import DownloadParser
from .sat_connector import SATConnector


class TooMuchDowloadsError(Exception):
    """No content downloaded, this can be caused by already dowload twice the same package"""


class Package:
    identifier: str
    request_type: RequestType

    binary: bytes
    cfdis: List[CFDI]

    request_status: int
    raw: bytes

    def __init__(self, package_id: str, request_type: RequestType):
        self.identifier = package_id
        self.request_type = request_type

    @classmethod
    def from_ids(cls, package_ids: List[str], request_type: RequestType) -> List["Package"]:
        return [cls(package_id, request_type) for package_id in package_ids]

    def download(self, connector: SATConnector, process: bool = True):
        data = self.soap_download()
        response = connector.download_package(data)
        self.raw = response.content
        if process:
            self._process_download_response(response)

    def soap_download(self) -> Dict[str, str]:
        """Creates the SOAP body to the verify request"""
        return {
            "package_id": self.identifier,
            "signature": "{signature}",
        }

    def _process_download_response(self, response: Response = None):
        # self.request_status = response.status_code
        # utils.check_response(response)
        content = response.content if response else self.raw
        response_clean = utils.remove_namespaces(content.decode("UTF-8"))
        parsed = DownloadParser.parse(response_clean)
        if not parsed["Content"]:
            raise TooMuchDowloadsError(
                "No content downloaded, this can be caused by already dowload twice the same package"
            )
        self.binary = base64.b64decode(parsed["Content"])
        if self.request_type == RequestType.CFDI:
            self.cfdis = XML2CFDI.from_binary(self.binary)
        elif self.request_type == RequestType.METADATA:
            self.cfdis = Metadata2CFDI.from_binary(self.binary)
        else:
            raise ValueError("Unkown request type")
