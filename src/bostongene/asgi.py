from contextlib import suppress

from fastapi import FastAPI, Response, status
from bostongene.heavy_calc import heavy_calc, backend
from dramatiq.results import ResultMissing

app = FastAPI()


@app.get("/calculate", status_code=status.HTTP_201_CREATED)
def calculate(x: float):
    message_id = heavy_calc.send(num=x).message_id
    return {"message_id": message_id}


@app.get("/result")
def result(message_id: str, response: Response):
    with suppress(ResultMissing):
        message = heavy_calc.message().copy(message_id=message_id)
        return {"result": backend.get_result(message)}

    response.status_code = status.HTTP_201_CREATED
