
from am_okay.domain.transfer_buffer import TransferBuffer
from am_okay.domain.transfer_operation import TransferOperation, TransferType



def test_transfer_buffer_initialization():
    """
    @overview Test case validating that `TransferBuffer` initializes with empty slots and no default operation.
    """

    transfer_buffer = TransferBuffer()


    assert transfer_buffer.slot_operations == {}
    assert transfer_buffer.default_operation is None



def test_set_and_get_slot_operation(empty_transfer_buffer, tmp_path):
    """
    @overview Test case validating the setting and retrieval of a slot operation.

    :param empty_transfer_buffer {TransferBuffer} - The fixture providing a `TransferBuffer` instance.
    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()

    transfer_operation = TransferOperation(TransferType.COPY, [str(file_path)])
    empty_transfer_buffer.set_slot_operation_at(0, transfer_operation)


    assert empty_transfer_buffer.get_slot_operation_at(0) == transfer_operation



def test_set_and_clear_slot_operation(empty_transfer_buffer, tmp_path):
    """
    @overview Test case validating the setting and clearing of a slot operation.

    :param empty_transfer_buffer {TransferBuffer} - The fixture providing a `TransferBuffer` instance.
    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()

    transfer_operation = TransferOperation(TransferType.COPY, [str(file_path)])
    empty_transfer_buffer.set_slot_operation_at(0, transfer_operation)
    empty_transfer_buffer.clear_slot_operation_at(0)


    assert empty_transfer_buffer.get_slot_operation_at(0) is None



def test_set_and_clear_default_operation(empty_transfer_buffer, tmp_path):
    """
    @overview Test case validating the setting and clearing of the default operation.

    :param empty_transfer_buffer {TransferBuffer} - The fixture providing a `TransferBuffer` instance.
    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()


    transfer_operation = TransferOperation(TransferType.COPY, [str(file_path)])
    empty_transfer_buffer.set_default_operation(transfer_operation)


    assert empty_transfer_buffer.default_operation == transfer_operation

    empty_transfer_buffer.clear_default_operation()
    
    assert empty_transfer_buffer.default_operation is None
