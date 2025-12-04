import os
import sys
import pytest


# Add project root to sys.path for tests run via pytest without -m
ROOT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(ROOT)
if PARENT not in sys.path:
    sys.path.insert(0, PARENT)


@pytest.fixture(scope="session", autouse=True)
def ensure_test_env():
    # Keep tests isolated from prod env by default
    os.environ.setdefault("DB_PROVIDER", "sqlite")
    return True
