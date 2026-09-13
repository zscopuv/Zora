import json
import time
import urllib.request
from pathlib import Path

from packaging.version import Version

from . import __version__


PYPI_URL = "https://pypi.org/pypi/zora-cli/json"

CHECK_INTERVAL = 60 * 60 * 24  # 24 hours


def _cache_file():
    return Path.home() / ".cache" / "zora" / "update.json"


def get_latest_version():
    try:
        request = urllib.request.Request(
            PYPI_URL,
            headers={
                "User-Agent": f"zora-cli/{__version__}"
            },
        )

        with urllib.request.urlopen(request, timeout=2) as response:
            data = json.load(response)

        return data["info"]["version"]

    except Exception:
        return None


def check_for_update():
    cache = _cache_file()

    try:
        if cache.exists():
            data = json.loads(cache.read_text())

            if time.time() - data["checked"] < CHECK_INTERVAL:
                latest = data.get("latest")

                if latest and Version(latest) > Version(__version__):
                    return latest

                return None
    except Exception:
        pass

    latest = get_latest_version()

    try:
        cache.parent.mkdir(parents=True, exist_ok=True)

        cache.write_text(
            json.dumps({
                "checked": time.time(),
                "latest": latest,
            })
        )
    except Exception:
        pass

    if latest and Version(latest) > Version(__version__):
        return latest

    return None