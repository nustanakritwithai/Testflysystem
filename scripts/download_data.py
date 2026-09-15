#!/usr/bin/env python3
"""Download the three MaleCNS v1.0 flat-connectome files used by Testflysystem.

Downloads are resumable and remain under data/raw/, which is gitignored.
Official source: Janelia MaleCNS Google Cloud Storage release bucket.
"""
from pathlib import Path
from urllib.request import Request, urlopen

BASE = "https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome"
FILES = [
    "connectome-weights-male-cns-v1.0-minconf-0.5.feather",
    "body-annotations-male-cns-v1.0-minconf-0.5.feather",
    "body-neurotransmitters-male-cns-v1.0.feather",
]


def download(url: str, destination: Path, chunk: int = 1024 * 1024) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    existing = destination.stat().st_size if destination.exists() else 0
    headers = {"Range": f"bytes={existing}-"} if existing else {}
    request = Request(url, headers=headers)
    with urlopen(request) as response:
        append = existing > 0 and response.status == 206
        mode = "ab" if append else "wb"
        if existing and not append:
            existing = 0
        with destination.open(mode) as out:
            while True:
                data = response.read(chunk)
                if not data:
                    break
                out.write(data)
    print(f"ready: {destination} ({destination.stat().st_size:,} bytes)")


def main() -> None:
    root = Path("data/raw")
    for name in FILES:
        download(f"{BASE}/{name}", root / name)


if __name__ == "__main__":
    main()
