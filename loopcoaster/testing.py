import sys
import time


# for testing, to be later removed or moved to tests

class DummyMotor:
    def __init__(self, port: str):
        self.port = port

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.port!r})'

    def plimit(self, plimit: float) -> None:
        self._log(f"setting plimit={plimit}")

    def run_for_rotations(self, rotations: float, speed: float) -> None:
        self._log(f"running rotations={rotations}, speed={speed}")
        time.sleep(abs(rotations) / speed * 10)

    def stop(self) -> None:
        self._log("stopped")

    def _log(self, obj):
        print(f">>> {self}: {obj}", file=sys.stderr)
