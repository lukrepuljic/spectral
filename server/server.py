import asyncio
import csv
import logging
import os
from typing import Generator

import grpc
from proto.electricity_consumption_pb2 import ConsumptionPoint, Request
from proto.electricity_consumption_pb2_grpc import (
    ElectricityConsumptionServicer as GRPCElectricityConsumptionServicer,
    add_ElectricityConsumptionServicer_to_server,
)

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s ", level=logging.INFO
)
logger = logging.getLogger(__name__)

DATA_PATH: str = "./resources/meterusage.csv"


class ElectricityConsumptionServicer(GRPCElectricityConsumptionServicer):
    """gRPC server class."""

    async def GetElectricityConsumption(self, request: Request, context):
        """gRPC method that returns a stream of messages
        representing measurements of electricity consumption.
        """
        request_id: str = request.id
        logger.info(f"Server: start request {request_id}")

        for timestamp, value in get_electricity_consumption_data(DATA_PATH):
            yield ConsumptionPoint(time=timestamp, measurement=value)

        logger.info(f"Server: start request {request_id}")


def get_electricity_consumption_data(
    data_path: str,
) -> Generator[tuple[str, float], None, None]:
    """Reads data from a .csv data defined with the given path
    and returns it as a stream.
    """
    with open(data_path, "r") as csv_file:
        for index, row in enumerate(csv.reader(csv_file)):
            if index == 0:
                continue
            yield row[0], float(row[1])


async def serve():
    """Runs the gRPC server."""
    server: grpc.aio.Server = grpc.aio.server()
    add_ElectricityConsumptionServicer_to_server(
        ElectricityConsumptionServicer(), server
    )
    server_port: str = os.environ.get("GRPC_SERVER_PORT")
    server.add_insecure_port(f"[::]:{server_port}")

    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(serve())
