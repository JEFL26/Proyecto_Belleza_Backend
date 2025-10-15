# app/utils/response_handler.py
from fastapi.responses import JSONResponse

class ResponseHandler:
    @staticmethod
    def success(data=None, message="Operación exitosa", status_code=200):
        return JSONResponse(
            status_code=status_code,
            content={"status": "success", "message": message, "data": data},
        )

    @staticmethod
    def bad_request(message="Solicitud inválida"):
        return JSONResponse(status_code=400, content={"status": "error", "message": message})

    @staticmethod
    def not_found(message="Recurso no encontrado"):
        return JSONResponse(status_code=404, content={"status": "error", "message": message})

    @staticmethod
    def accepted(message="Solicitud aceptada"):
        return JSONResponse(status_code=202, content={"status": "accepted", "message": message})

    @staticmethod
    def server_error(message="Error interno del servidor"):
        return JSONResponse(status_code=500, content={"status": "error", "message": message})


# Alias prácticos (para importar directo)
response_success = ResponseHandler.success
response_error = ResponseHandler.server_error