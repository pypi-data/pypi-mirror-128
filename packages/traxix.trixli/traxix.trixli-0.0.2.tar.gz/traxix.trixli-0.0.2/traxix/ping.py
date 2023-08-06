import time
import re
from dataclasses import dataclass, asdict
import json

from fire import Fire
import subprocess  # noqa: S404


@dataclass
class PingResult:
    _status: bool
    _time: float = 0
    _min: float = 0
    _max: float = 0
    _avg: float = 0
    _mdev: float = 0

    def __post_init__(self):
        self._time = time.time()

    def to_json(self):
        return asdict(self)


def _ping_one(host):
    r = subprocess.run(  # noqa: S603
        ["/usr/bin/ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE
    )

    if r.returncode != 0:
        print("command failed")
        return PingResult(_status=False)

    output = r.stdout
    # rtt min/avg/max/mdev = 91.209/91.209/91.209/0.000 ms
    line = output.decode().split("\n")[-2]

    groups = re.match(
        r"rtt min/avg/max/mdev = (?P<min>[0-9\.]+)/(?P<avg>[0-9\.]+)/(?P<max>[0-9\.]+)/(?P<mdev>[0-9\.]+) .*",
        line,
    )

    if groups is None:
        print("regexp failed")
        return PingResult(_status=False)

    return PingResult(
        _status=True,
        _min=float(groups.groupdict()["min"]),
        _max=float(groups.groupdict()["max"]),
        _avg=float(groups.groupdict()["avg"]),
        _mdev=float(groups.groupdict()["mdev"]),
    )


def ping(host="8.8.8.8", log_path="/home/trax/perso/telemerde.json"):
    log = open(log_path, "a")
    while True:
        result = _ping_one(host).to_json()
        print(result)
        log.write(json.dumps(result))
        log.write("\n")
        log.flush()
        time.sleep(1)


if __name__ == "__main__":
    Fire(ping)
