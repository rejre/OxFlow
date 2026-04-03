"""Test configuration and fixtures."""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def temp_config_dir(tmp_path):
    """Provide a temporary config directory."""
    config_dir = tmp_path / ".oxflow"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def sample_url():
    """Provide sample URLs for testing."""
    return {
        "youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "bilibili": "https://www.bilibili.com/video/BV1GJ411x7p7",
        "direct_file": "https://github.com/rejre/OxFlow/releases/download/v1.0/OxFlow.dmg",
    }
