from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback


def setup_middleware(app: FastAPI) -> None:
    """
    Daftarkan semua middleware custom di sini.
    Buat masa ini, kita tambah global exception handler ringkas.
    """

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        """
        Contoh middleware ringkas jika Aca mahu log masa proses.
        Buat masa ini, hanya pass-through tanpa log berat.
        """
        response = await call_next(request)
        return response

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """
        Tangani error tak dijangka supaya server tidak crash tanpa respon.
        Untuk development, kita boleh log stack trace ke console.
        Untuk production, sebaiknya log ke sistem logging.
        """
        print("❌ Unhandled exception caught in global_exception_handler")
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Ralat dalaman server. Sila cuba lagi.",
                "detail": str(exc),
            },
        )
