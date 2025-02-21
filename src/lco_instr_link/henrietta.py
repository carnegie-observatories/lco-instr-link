import time
from lco_instr_link.lco_instr_link import LcoInstrLink


class Henrietta(LcoInstrLink):

    EXPOSURE_TIMEOUT = 4  # exposure must finish in 4 seconds after exposure time
    EXPOSURE_MAX_DIFF = 1  # exposure time must be set within 1 second of requested time

    def __init__(self, ip: str = "localhost", port: int = 52801):
        super().__init__(ip, port)

    def get_version(self) -> str:
        return self.get("version")

    def _get_status(self) -> str:
        st = self.get("status").split()
        return {"exposing": bool(int(st[0])), "moving": bool(int(st[1]))}

    def is_moving(self) -> bool:
        return self._get_status()["moving"]

    def is_exposing(self) -> bool:
        return self._get_status()["exposing"]

    def expose(self, seconds: int, count: int = 1) -> bool:
        # set exposure time
        exptime = self.get_float(f"exptime {seconds}")
        if exptime < seconds - self.EXPOSURE_MAX_DIFF or exptime > seconds + self.EXPOSURE_MAX_DIFF:
            raise Exception("Error setting exposure time")
        # start exposure
        if count > 1:
            cmd = "start %d" % count
        else:
            cmd = "start"
        if "ok" not in self.get(cmd):
            raise Exception("Error starting exposure")
        # wait for exposure to finish
        start = time.time()
        while self.is_exposing():
            if time.time() - start > (exptime + self.EXPOSURE_TIMEOUT) * count:
                raise Exception("Exposure timeout")
            time.sleep(1)
        return True
