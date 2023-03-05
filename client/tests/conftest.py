from unittest.mock import Mock

import pytest


@pytest.fixture()
def grpc_stub():
    stub = Mock()
    stub.GetElectricityConsumption = Mock()

    return stub
