#!/usr/bin/env python3
from __future__ import annotations

import http.client
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]


def free_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def request(port: int, method: str, path: str, body: bytes = b"") -> tuple[int, bytes]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
    connection.request(method, path, body=body, headers={"Content-Length": str(len(body))})
    response = connection.getresponse()
    result = response.status, response.read()
    connection.close()
    return result


def main() -> int:
    hhy = os.environ.get("HHY", "hhy")
    port = free_port()
    process = subprocess.Popen(
        [hhy, "serve", str(ROOT / "examples/api/app.hhy"), "--", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(process.stderr.read())
            try:
                status, body = request(port, "GET", "/")
                if status == 200:
                    break
            except OSError:
                time.sleep(0.05)
        else:
            raise RuntimeError("server did not become ready")

        assert json.loads(body) == {"ok": True, "service": "books"}
        status, body = request(port, "GET", "/api/books/42")
        assert status == 200 and json.loads(body)["id"] == "42"
        status, body = request(port, "POST", "/api/books", b'{"title":"HHY"}')
        assert status == 201 and json.loads(body)["book"]["title"] == "HHY"
        assert request(port, "POST", "/api/books", b"{")[0] == 400
        assert request(port, "GET", "/admin")[0] == 403
        assert request(port, "GET", "/healthz")[0] == 200
        assert request(port, "GET", "/metrics")[0] == 200
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=2)
    print("HHY Web smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
