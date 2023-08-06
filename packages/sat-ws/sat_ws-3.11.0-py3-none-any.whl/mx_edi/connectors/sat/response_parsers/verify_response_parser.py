from typing import Any, Dict

import xmltodict

from .response_parser import ResponseParser


class VerifyParser(ResponseParser):
    @staticmethod
    def parse(response: str) -> Dict[str, Any]:
        """Gets the Query ID from the raw response"""
        response_dict = xmltodict.parse(response)
        result = response_dict["Envelope"]["Body"]["VerificaSolicitudDescargaResponse"][
            "VerificaSolicitudDescargaResult"
        ]
        return {
            "EstadoSolicitud": result["@EstadoSolicitud"],
            "CodEstatus": result["@CodEstatus"],
            "Mensaje": result["@Mensaje"],
            "CodigoEstadoSolicitud": result.get("@CodigoEstadoSolicitud", 0),
            "NumeroCFDIs": result.get("@NumeroCFDIs", 0),
            "IdsPaquetes": [result["IdsPaquetes"]]
            if result["@EstadoSolicitud"] == "3"
            else [],  # TODO Check what happens when multiple ids
        }
