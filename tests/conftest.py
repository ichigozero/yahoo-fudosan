import time

import pytest


@pytest.fixture
def sleep_mock(monkeypatch):
    def sleep(seconds):
        pass

    monkeypatch.setattr(time, 'sleep', sleep)
