"""Tests."""

import os

from htmloverpdf import render


def test_render_blank() -> None:
    """Test an empty doc."""
    assert bytes(render("<html />"))[:8] == b"%PDF-1.5"


def test_render() -> None:
    """Test a pdf."""
    assert (
        bytes(
            render(
                f"""<html><body>
  <img src="file://{os.getcwd()}/tests/empty.pdf" />
  <p>Test</p>
  <img src="blank.pdf" />
  <p>Test</p>
  <img src="file://{os.getcwd()}/tests/empty.pdf" />
</body></html>"""
            )
        )[:8]
        == b"%PDF-1.5"
    )
