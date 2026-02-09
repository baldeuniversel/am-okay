
import os
from pathlib import Path
from typing import List

from am_okay.domain.transfer_operation import TransferType



def validate_source_path(paths: List[Path], transfer_type: TransferType):
    """
    @overview A function that allows validating source paths before preparing a transfer operation.

    General responsibilities:
      - Ensure all source paths exist
      - Ensure source paths are readable (files or dirs)
      - Ensure source paths are files or directories
      - For `CUT` operations, ensure that the parent directories of the source files or directories are writable

    @details This validation is performed during the *prepare* phase and prevents
    invalid operations from being stored in the buffer repository.

    :param paths {List[Path]} - The list of source paths to validate (files or dirs).
    :param transfer_type {TransferType} - The transfer type (`COPY` or `CUT`).

    :raises {ValueError} - If a source does not exist or is invalid.
    :raises {PermissionError} - If permissions are insufficient.
    """

    for path in paths:

        if not path.exists():
            raise ValueError(f"\nSource does not exist: {path}  🧐")

        if not path.is_file() and not path.is_dir():
            raise ValueError(f"\nUnsupported source type: {path}  ❗")

        if not os.access(path, os.R_OK):
            raise PermissionError(f"\nRead permission denied: {path}  ⛔")

        
        #
        if transfer_type is TransferType.CUT:

            parent = path.parent

            if not os.access(parent, os.W_OK):
                raise PermissionError(f"\nWrite permission denied on parent directory: {parent}  ⛔")



def validate_destination_dir(destination_dir: Path):
    """
    @overview A function that allows validating the destination directory before executing a transfer.

    General responsibilities:
      - Ensure destination dir exists
      - Ensure destination dir is a directory
      - Ensure destination dir is writable

    @detail This validation is performed at *execution* time and prevents
    partial or corrupted transfers.

    :param destination_dir {Path} - Target directory for the transfer.

    :raises {ValueError} - If destination dir is invalid.
    :raises {PermissionError} - If write permission is missing.
    """

    if not destination_dir.exists():
        raise ValueError(f"\nDestination does not exist: {destination_dir}  🧐")

    if not destination_dir.is_dir():
        raise ValueError(f"\nDestination is not a directory: {destination_dir}  🧐")


    #
    if not os.access(destination_dir, os.W_OK):
        raise PermissionError(f"\nWrite permission denied: {destination_dir}  ⛔")
