import logging
import math
import os
import uuid
from typing import Union

import grpc
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from proto.electricity_consumption_pb2 import Request as GrpcRequest
from proto.electricity_consumption_pb2_grpc import ElectricityConsumptionStub

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s ", level=logging.INFO
)
logger = logging.getLogger(__name__)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


class GrpcClient:
    """gRPC client class."""

    def __init__(self) -> None:
        server_host: str = os.environ.get("GRPC_SERVER_HOST")
        server_port: str = os.environ.get("GRPC_SERVER_PORT")

        self._channel: grpc.Channel = grpc.insecure_channel(
            f"{server_host}:{server_port}"
        )
        self.stub: ElectricityConsumptionStub = ElectricityConsumptionStub(
            self._channel
        )

    def close(self) -> None:
        """Closes the gRPC channel between the client and the server."""
        self._channel.close()


@app.on_event("startup")
async def startup_event():
    """Adds the gRPC client to the state."""
    app.state.grpc_client = GrpcClient()


@app.on_event("shutdown")
async def shutdown_event():
    """Closes the gRPC client."""
    app.state.grpc_client.close()


async def get_stub(request: Request) -> ElectricityConsumptionStub:
    """GRPC Service to be injected."""
    return request.app.state.grpc_client.stub


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """Home endpoint,
    returns an HTML document.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/measurements/")
async def get_data(
    stub: ElectricityConsumptionStub = Depends(get_stub),
):
    """Endpoint that returns electricity consumption data."""
    request_id = str(uuid.uuid4())
    logger.info(f"Client: start request {request_id}")
    request: GrpcRequest = GrpcRequest(id=request_id)

    response_data: list[dict[str, Union[str, float]]] = []
    for measurement in stub.GetElectricityConsumption(request):
        time: str = measurement.time
        value: float = (
            round(measurement.measurement, 2)
            if not math.isnan(measurement.measurement)
            else None
        )
        response_data.append({"time": time, "value": value})

    logger.info(f"Client: end request {request_id}")

    return response_data
