from typing import AsyncGenerator
from unittest.mock import create_autospec

import grpc
import pytest

from ..proto.electricity_consumption_pb2 import ConsumptionPoint, Request
from ..server import ElectricityConsumptionServicer


def request_generator():
    return Request(id="test_id")


@pytest.mark.asyncio
async def test_servicer():
    servicer = ElectricityConsumptionServicer()
    request = request_generator()
    mock_context = create_autospec(spec=grpc.aio.ServicerContext)

    resposen: AsyncGenerator = servicer.GetElectricityConsumption(request, mock_context)
    result: list[ConsumptionPoint] = [x async for x in resposen]

    assert len(result) == 2975
    assert isinstance(result[0], ConsumptionPoint)
