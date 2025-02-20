import pytest
from lco_instr_link.lco_instr_link import LcoInstrLink


class TestLcoInstrLink:

    @pytest.fixture()
    def link(self):
        link = LcoInstrLink()
        link.connect()
        yield link
        link.close()

    def test_connection(self, link):
        assert link.ping()

    def test_get(self, link):
        assert "Alpha" in link.get("version")  # fixme
