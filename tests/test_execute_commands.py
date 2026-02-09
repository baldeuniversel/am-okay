
from am_okay.application.execute_commands import PasteCommand
from am_okay.domain.transfer_operation import TransferOperation, TransferType



def test_execute_copy_default(empty_transfer_buffer, temp_buffer_repo, progress_observer, tmp_path):
    """
    @overview Test case validating the execution of the default operation.

    :param empty_transfer_buffer {TransferBuffer} - The fixture providing a `TransferBuffer` instance.
    :param temp_buffer_repo {BufferRepository} - The fixture providing a `BufferRepository` instance.
    :param progress_observer {TqdmProgressObserver} - The fixture providing a `ProgressObserver` instance.
    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()

    transfer_operation = TransferOperation(TransferType.COPY, [str(file_path)])
    empty_transfer_buffer.set_default_operation(transfer_operation)
    paste_cmd = PasteCommand(empty_transfer_buffer, temp_buffer_repo, progress_observer)

    dest_path = tmp_path / "dest"
    dest_path.mkdir()

    paste_cmd.execute_default(dest_path)


    assert (dest_path / "test_file").exists()



def test_execute_copy_slot_at(empty_transfer_buffer, temp_buffer_repo, progress_observer, tmp_path):
    """
    @overview Test case validating the execution of a slot operation.

    :param empty_transfer_buffer {TransferBuffer} - The fixture providing a `TransferBuffer` instance.
    :param temp_buffer_repo {BufferRepository} - The fixture providing a `BufferRepository` instance.
    :param progress_observer {TqdmProgressObserver} - The fixture providing a `ProgressObserver` instance.
    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()

    transfer_operation = TransferOperation(TransferType.COPY, [str(file_path)])
    empty_transfer_buffer.set_slot_operation_at(0, transfer_operation)
    paste_cmd = PasteCommand(empty_transfer_buffer, temp_buffer_repo, progress_observer)

    dest_path = tmp_path / "dest"
    dest_path.mkdir()

    paste_cmd.execute_slot_at(0, dest_path)


    assert (dest_path / "test_file").exists()



def test_execute_cut_default(empty_transfer_buffer, temp_buffer_repo, progress_observer, tmp_path):
    """
    @overview Test case validating the execution of the default `CUT` operation.

    :param empty_transfer_buffer {TransferBuffer} - The fixture providing a `TransferBuffer` instance.
    :param temp_buffer_repo {BufferRepository} - The fixture providing a `BufferRepository` instance.
    :param progress_observer {TqdmProgressObserver} - The fixture providing a `ProgressObserver` instance.
    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()

    transfer_operation = TransferOperation(TransferType.CUT, [str(file_path)])
    empty_transfer_buffer.set_default_operation(transfer_operation)
    paste_cmd = PasteCommand(empty_transfer_buffer, temp_buffer_repo, progress_observer)

    dest_path = tmp_path / "dest"
    dest_path.mkdir()

    paste_cmd.execute_default(dest_path)


    assert (dest_path / "test_file").exists()
    assert not file_path.exists()



def test_execute_cut_slot_at(empty_transfer_buffer, temp_buffer_repo, progress_observer, tmp_path):
    """
    @overview Test case validating the execution of a `CUT` slot operation.

    :param empty_transfer_buffer {TransferBuffer} - The fixture providing a `TransferBuffer` instance.
    :param temp_buffer_repo {BufferRepository} - The fixture providing a `BufferRepository` instance.
    :param progress_observer {TqdmProgressObserver} - The fixture providing a `ProgressObserver` instance.
    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()

    transfer_operation = TransferOperation(TransferType.CUT, [str(file_path)])
    empty_transfer_buffer.set_slot_operation_at(0, transfer_operation)
    paste_cmd = PasteCommand(empty_transfer_buffer, temp_buffer_repo, progress_observer)

    dest_path = tmp_path / "dest"
    dest_path.mkdir()

    paste_cmd.execute_slot_at(0, dest_path)


    assert (dest_path / "test_file").exists()
    assert not file_path.exists()
