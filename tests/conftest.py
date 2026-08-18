"""Pytest configuration for the MAX plugin test suite.

The tests import the adapter via ``load_plugin_adapter("max")``, which
resolves ``plugins/platforms/max/adapter.py`` relative to the **Hermes
Agent repo root** (the loader lives at ``tests/gateway/_plugin_adapter_loader.py``
and derives ``_REPO_ROOT`` from its own file location).

For a standalone repo (this one) the adapter lives in *this* repo at
``plugins/platforms/max/adapter.py`` — so we inject a shim that teaches
the loader where to find it, and make ``tests.gateway`` importable so
the ``_plugin_adapter_loader`` import inside the test files resolves.

Two supported contexts:

1. **Inside a hermes-agent checkout** (CI / PR branch) — this conftest
   is inert: the real ``tests.gateway._plugin_adapter_loader`` already
   exists and resolves the plugin from the agent's own tree.

2. **Standalone** (this repo, ``D:\\GITHUB\\max-hermes-plugin``) — we
   register a synthetic ``tests.gateway`` package whose
   ``_plugin_adapter_loader.load_plugin_adapter`` points at this repo's
   ``plugins/platforms/max`` directory.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]          # repo root
_PLUGIN_DIR = _REPO_ROOT / "plugins" / "platforms" / "max"


def _real_loader_available() -> bool:
    """True when running inside a hermes-agent checkout (has its own loader)."""
    try:
        import tests.gateway._plugin_adapter_loader  # noqa: F401
        return True
    except ModuleNotFoundError:
        return False


def _install_standalone_loader() -> None:
    """Create a minimal ``tests.gateway._plugin_adapter_loader`` shim."""
    pkg = types.ModuleType("tests")
    pkg.__path__ = []  # type: ignore[attr-defined]
    sys.modules.setdefault("tests", pkg)

    gw = types.ModuleType("tests.gateway")
    gw.__path__ = []  # type: ignore[attr-defined]
    sys.modules.setdefault("tests.gateway", gw)

    loader_mod = types.ModuleType("tests.gateway._plugin_adapter_loader")

    def load_plugin_adapter(plugin_name: str):
        module_name = f"plugin_adapter_{plugin_name}"
        cached = sys.modules.get(module_name)
        if cached is not None:
            return cached
        adapter_path = _PLUGIN_DIR / "adapter.py"
        if not adapter_path.is_file():
            raise FileNotFoundError(
                f"Plugin adapter not found: {adapter_path}."
            )
        # Insert the plugin dir on sys.path so its own imports
        # (gateway.*, agent.*) resolve from the hermes-agent venv
        sys.path.insert(0, str(_PLUGIN_DIR.parent.parent.parent))  # repo root
        spec = importlib.util.spec_from_file_location(module_name, adapter_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    loader_mod.load_plugin_adapter = load_plugin_adapter
    sys.modules["tests.gateway._plugin_adapter_loader"] = loader_mod


if not _real_loader_available():
    _install_standalone_loader()