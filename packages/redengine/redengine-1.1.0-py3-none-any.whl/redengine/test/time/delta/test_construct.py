
import pytest
import pandas as pd
from redengine.core.time import (
    TimeDelta
)

@pytest.mark.parametrize(
    "offset,expected",
    [
        pytest.param(
            "10:20:30",
            pd.Timedelta(hours=10, minutes=20, seconds=30),
            id="String"),
    ],
)
def test_construct(offset, expected):
    time = TimeDelta(offset)
    assert expected == time.past

