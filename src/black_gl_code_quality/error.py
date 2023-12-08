import hashlib
from typing import Any, Mapping


def validate_severity(val: str) -> bool:
    return val.lower() in ("info", "minor", "major", "critical", "blocker")


def file_fingerprint(path: str) -> str:
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def generate_error(path: str, severity: str) -> Mapping[str, Any]:
    err = {
        "type": "issue",
        "description": "Black would reformat",
        "check_name": "inconsistent-format",
        "category": [
            "Style",
        ],
        "location": {
            "lines": {"begin": 1, "end": 1},
            "path": path,
        },
        "fingerprint": file_fingerprint(path),
        "severity": severity,
    }

    return err
