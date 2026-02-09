
from pathlib import Path
from typing import List



def normalize_paths(paths: List[str]) -> List[Path]:
    """
    @overview A function to normalize and resolve input paths.

    Responsibilities:
      - Expand user (~)
      - Resolve absolute paths
      - Return Path objects (domain-friendly)

    :param paths {List[str]} - The raw input paths.

    :return {List[Path]} - Normalized Path objects

    :raises {FileNotFoundError} - A file not found exception.
    """

    normalized: List[Path] = []


    for current_path in paths:

        target_path = Path(current_path).expanduser().resolve()

        if not target_path.exists():
            raise FileNotFoundError(f"\nPath does not exist: {target_path}  🧐")
        
        normalized.append(target_path)


    return normalized
