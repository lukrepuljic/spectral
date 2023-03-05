from collections import namedtuple
from typing import Union

import pytest
from fastapi import Request, Response
from fastapi.testclient import TestClient

from ..client import app, get_stub

client = TestClient(app)


def test_get_home():
    response: Response = client.get("/")

    assert response.status_code == 200
    assert response.template.name == "index.html"


@pytest.mark.parametrize(
    "measurements",
    [
        (
            [
                {"time": "2023-03-01 01:00:00,00.00", "value": 139.22},
                {"time": "2023-03-01 01:01:00,00.00", "value": 138.75},
                {"time": "2023-04-01 02:00:00,00.00", "value": 140.25},
            ]
        )
    ],
)
def test_get_data(grpc_stub, measurements: list[dict[str, Union[str, float]]]):
    async def override_dependency(request: Request) -> None:
        Point = namedtuple("Point", "time measurement")
        mock_measurements: list[Point] = [
            Point(point["time"], point["value"]) for point in measurements
        ]
        grpc_stub.GetElectricityConsumption.return_value = mock_measurements

        return grpc_stub

    app.dependency_overrides[get_stub] = override_dependency

    response: Response = client.get("/measurements")

    assert response.status_code == 200
    assert response.json() == measurements
