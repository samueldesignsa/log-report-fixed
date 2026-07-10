"""Verifier for dynamo/log-report.

Each test maps 1:1 to a numbered success criterion in instruction.md. Expected
values are recomputed directly from /app/access.log, so the verifier checks the
real outcome rather than merely that a file exists.
"""
import json
import re
from collections import Counter
from pathlib import Path

import pytest

REPORT = Path("/app/report.json")
LOG = Path("/app/access.log")

REQUIRED_KEYS = {"total_requests", "unique_ips", "top_path"}
METHODS = ("GET", "POST", "PUT", "DELETE", "HEAD", "PATCH", "OPTIONS", "TRACE", "CONNECT")


def _expected():
    """Ground-truth summary computed directly from the log."""
    paths, ips, total = Counter(), set(), 0
    pat = re.compile(r'"(?:%s) (\S+) ' % "|".join(METHODS))
    for line in LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        m = pat.search(line)
        if m:
            paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0] if paths else None,
    }


@pytest.fixture(scope="module")
def report():
    return json.loads(REPORT.read_text())


def test_report_exists_and_valid_json():
    """Criterion 1: /app/report.json exists and contains valid JSON."""
    assert REPORT.exists(), "no /app/report.json found"
    assert REPORT.stat().st_size > 0, "report.json is empty"
    json.loads(REPORT.read_text())  # raises if not valid JSON


def test_schema_and_types(report):
    """Criterion 2: object with exactly the three keys and the required types."""
    assert isinstance(report, dict), "report.json must be a JSON object"
    assert set(report.keys()) == REQUIRED_KEYS, (
        f"keys must be exactly {sorted(REQUIRED_KEYS)}, got {sorted(report.keys())}"
    )
    assert isinstance(report["total_requests"], int) and not isinstance(
        report["total_requests"], bool
    ), "total_requests must be an integer"
    assert isinstance(report["unique_ips"], int) and not isinstance(
        report["unique_ips"], bool
    ), "unique_ips must be an integer"
    assert isinstance(report["top_path"], str), "top_path must be a string"


def test_total_requests(report):
    """Criterion 3: total_requests equals the number of requests in the log."""
    assert report["total_requests"] == _expected()["total_requests"]


def test_unique_ips(report):
    """Criterion 4: unique_ips equals the number of distinct client IPs."""
    assert report["unique_ips"] == _expected()["unique_ips"]


def test_top_path(report):
    """Criterion 5: top_path equals the most-requested path."""
    assert report["top_path"] == _expected()["top_path"]
