import os
from pathlib import Path


def pytest_sessionstart(session):
    """Ensure a clean SQLite DB before running tests."""
    repo_root = Path(__file__).resolve().parents[1]
    db_path = repo_root / "products.db"
    try:
        if db_path.exists():
            db_path.unlink()
    except Exception:
        # best-effort removal; tests will still run but may fail if DB locked
        pass
