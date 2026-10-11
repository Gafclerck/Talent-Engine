"""Demarrage a froid : uvicorn sert l'application sans service externe (AD-11, NFR8)."""

import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]


def _port_libre() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_libre:
        socket_libre.bind(("127.0.0.1", 0))
        return socket_libre.getsockname()[1]


def test_demarrage_a_froid_sert_la_route_de_sante() -> None:
    port = _port_libre()
    processus = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--log-level",
            "warning",
        ],
        cwd=RACINE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    url = f"http://127.0.0.1:{port}/sante"
    try:
        reponse: tuple[int, dict[str, str]] | None = None
        for _ in range(100):
            if processus.poll() is not None:
                sortie = processus.stdout.read() if processus.stdout else ""
                raise AssertionError(f"uvicorn s'est arrete prematurement:\n{sortie}")
            try:
                with urllib.request.urlopen(url, timeout=0.5) as flux:
                    reponse = (flux.status, json.loads(flux.read().decode("utf-8")))
                break
            except (urllib.error.URLError, OSError):
                time.sleep(0.1)
        assert reponse == (200, {"statut": "ok"}), "l'application n'a pas repondu dans le delai imparti"
    finally:
        processus.terminate()
        try:
            processus.wait(timeout=10)
        except subprocess.TimeoutExpired:
            processus.kill()
            processus.wait(timeout=10)
