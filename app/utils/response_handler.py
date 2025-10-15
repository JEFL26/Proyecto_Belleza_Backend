# app/utils/response_handler.py
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder   # 👈 Importa esto
from fastapi import status

class ResponseHandler:
    @staticmethod
    def success(data=None, message="Operación exitosa", status_code=status.HTTP_200_OK):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "success",
                "message": message,
                "data": jsonable_encoder(data),  # 👈 Aquí la magia
            },
        )

    @staticmethod
    def bad_request(message="Solicitud inválida"):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": message},
        )

    @staticmethod
    def not_found(message="Recurso no encontrado"):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": "error", "message": message},
        )

    @staticmethod
    def accepted(message="Solicitud aceptada"):
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={"status": "accepted", "message": message},
        )

    @staticmethod
    def server_error(message="Error interno del servidor"):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": message},
        )


# Alias prácticos
response_success = ResponseHandler.success
response_bad_request = ResponseHandler.bad_request
response_not_found = ResponseHandler.not_found
response_accepted = ResponseHandler.accepted
response_error = ResponseHandler.server_error
