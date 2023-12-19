from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers.controllers import router as controllers
from app.exception.custom_exception import CsvValueException


app = FastAPI(
    version="0.9 beta",
)

app.include_router(controllers)


@app.exception_handler(CsvValueException)
async def unicorn_exception_handler(request: Request, exc: CsvValueException):
    return JSONResponse(
        status_code=500,
        content={
            "message": f"The input '{exc.value}' is in string format. Please convert it to a numeric value."
        },
    )
