"""HTTP shim for clinical-informatics.

Some notebooks need to call out to a FHIR server (hapi.fhir.org). The
shim makes the same call work in two environments:

- **Locally or in Codespaces.** We use ``requests``.
- **In a WASM Marimo runtime (e.g. marimo notebooks hosted statically).**
  We use ``pyodide.http.pyfetch`` because the browser can't run a
  synchronous ``requests`` call.

Either way, the public surface is ``fhir_get(url, params=None)`` and
``fhir_search(base, resource, params)`` returning parsed JSON.
"""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode


def _is_pyodide() -> bool:
    try:
        import sys

        return "pyodide" in sys.modules
    except Exception:  # noqa: BLE001
        return False


def fhir_get(url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """GET a JSON FHIR endpoint. Works locally and in Pyodide/WASM."""
    if _is_pyodide():
        return _pyodide_get(url, params)
    return _requests_get(url, params)


def fhir_search(
    base: str, resource: str, params: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Search a FHIR resource. Returns a parsed Bundle.

    Example::

        fhir_search(
            "https://hapi.fhir.org/baseR4",
            "Observation",
            {"code": "1988-5", "_count": 20},
        )
    """
    base = base.rstrip("/")
    url = f"{base}/{resource}"
    return fhir_get(url, params)


def _requests_get(url: str, params: dict[str, Any] | None) -> dict[str, Any]:
    import requests

    headers = {
        "Accept": "application/fhir+json",
        "User-Agent": "clinical-informatics/0.1",
    }
    resp = requests.get(url, params=params or {}, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _pyodide_get(url: str, params: dict[str, Any] | None) -> dict[str, Any]:
    # In WASM Marimo, this module runs sync. We construct a URL with query
    # string and synchronously block on pyfetch, pyodide's fetch wrapper.
    # When this runs in an async-only environment, the caller should
    # `await fhir_get_async` instead.
    from pyodide.http import open_url  # type: ignore[import-not-found]

    if params:
        url = f"{url}?{urlencode(params)}"
    raw = open_url(url).read()
    return json.loads(raw)


async def fhir_get_async(url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Async variant for WASM environments where you can ``await``."""
    if _is_pyodide():
        from pyodide.http import pyfetch  # type: ignore[import-not-found]

        if params:
            url = f"{url}?{urlencode(params)}"
        resp = await pyfetch(
            url,
            method="GET",
            headers={
                "Accept": "application/fhir+json",
                "User-Agent": "clinical-informatics/0.1",
            },
        )
        text = await resp.string()
        return json.loads(text)
    return _requests_get(url, params)
