from pathlib import Path
from typing import Any, List, Mapping, Sequence

from black_gl_code_quality.error import generate_error


def parse_simple_mode(data: List[str], severity: str) -> Sequence[Mapping[str, Any]]:
    errors = []
    magic_word = "would reformat"

    for line in data:
        if line.startswith(magic_word):
            path = Path(line.removeprefix(magic_word).strip()).relative_to(Path.cwd())
            errors.append(generate_error(str(path), severity))

    return errors
