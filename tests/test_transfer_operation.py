
from am_okay.domain.transfer_operation import TransferOperation, TransferType



def test_transfer_operation_initialization(tmp_path):
    """
    @overview Test case validating that `TransferOperation` initializes with 
    the correct type and paths.

    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()

    transfer_operation = TransferOperation(TransferType.COPY, [str(file_path)])


    assert transfer_operation.transfer_type == TransferType.COPY
    assert transfer_operation.source_paths == [str(file_path)]



def test_is_copy_operation(tmp_path):
    """
    @overview Test case validating the `*is_copy_operation*` scenario.

    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()

    transfer_operation = TransferOperation(TransferType.COPY, [str(file_path)])


    assert transfer_operation.is_copy_operation()
    assert not transfer_operation.is_cut_operation()



def test_is_cut_operation(tmp_path):
    """
    @overview Test case validating the `*is_cut_operation*` scenario.

    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()

    transfer_operation = TransferOperation(TransferType.CUT, [str(file_path)])


    assert transfer_operation.is_cut_operation()
    assert not transfer_operation.is_copy_operation()
