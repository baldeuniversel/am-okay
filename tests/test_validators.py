
from am_okay.domain.validators import validate_source_path, validate_destination_dir
from am_okay.domain.transfer_operation import TransferType



def test_validate_source_path(tmp_path):
    """
    @overview Test case validating source path handling for `COPY` and `CUT` operations.

    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()


    validate_source_path([file_path], TransferType.COPY)
    validate_source_path([file_path], TransferType.CUT)



def test_validate_destination_dir(tmp_path):
    """
    @overview Test case validating the destination directory.

    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()


    validate_destination_dir(dir_path)
