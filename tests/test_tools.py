"""Tests for tools"""

import sys
sys.path.insert(0, "src")

from my_mcp.tools.calculator import add, subtract
from my_mcp.tools.text_tools import reverse_text, uppercase_text


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5


def test_reverse_text():
    assert reverse_text("hello") == "olleh"
    assert reverse_text("mcp") == "pcm"


def test_uppercase_text():
    assert uppercase_text("hello") == "HELLO"
    assert uppercase_text("MCP") == "MCP"