import time
import pytest

from lco_instr_link.henrietta import Henrietta


class TestHenrietta:

    @pytest.fixture()
    def instrument(self):
        link = Henrietta()
        link.connect()
        yield link
        link.close()

    def test_status(self, instrument):
        status = instrument._get_status()
        assert "exposing" in status
        assert "moving" in status
        assert not status["exposing"]
        assert not status["moving"]

    def test_is_moving(self, instrument):
        assert not instrument.is_moving()

    def test_is_exposing(self, instrument):
        assert not instrument.is_exposing()

    def test_expose(self, instrument):
        t0 = time.time()
        # single exposure
        out = instrument.expose(5)
        assert out
        assert time.time() - t0 > 5
        t0 = time.time()
        # two exposures
        out = instrument.expose(5, 2)
        assert out
        assert time.time() - t0 > 10
