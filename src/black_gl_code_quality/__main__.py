#!/bin/env python

import json
import os
import subprocess
import sys
from io import StringIO
from typing import TextIO

from black_gl_code_quality.error import validate_severity
from black_gl_code_quality.parser import parse_simple_mode


def main():
    output = []
    stdin: TextIO = sys.stdin
    severity = os.environ.get("BLACK_GL_SEVERITY", "major").lower()
    exit_code = 0

    if not validate_severity(severity):
        severity = "major"

    if not stdin.closed:
        res = subprocess.run(
            ["black", "--check", *sys.argv[1:]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        exit_code = res.returncode
        stdin = StringIO(res.stderr.decode("utf-8"))

    output = parse_simple_mode(stdin.readlines(), severity)
    print(json.dumps(output))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
