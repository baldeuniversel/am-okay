
from am_okay.application.prepare_commands import PrepareCopyCommand, PrepareCutCommand
from am_okay.domain.transfer_operation import TransferType



def test_prepare_copy_command(empty_transfer_buffer, temp_buffer_repo, tmp_path):
    """
    @overview Test case validating the preparation of a `COPY` operation.

    :param empty_transfer_buffer {TransferBuffer} - The fixture providing a `TransferBuffer` instance.
    :param temp_buffer_repo {BufferRepository} - The fixture providing a `BufferRepository` instance.
    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()

    prepare_copy_cmd = PrepareCopyCommand(empty_transfer_buffer, temp_buffer_repo)
    prepare_copy_cmd.prepare([str(file_path)])


    assert empty_transfer_buffer.default_operation.transfer_type == TransferType.COPY



def test_prepare_cut_command(empty_transfer_buffer, temp_buffer_repo, tmp_path):
    """
    @overview Test case validating the preparation of a `CUT` operation.

    :param empty_transfer_buffer {TransferBuffer} - The fixture providing a `TransferBuffer` instance.
    :param temp_buffer_repo {BufferRepository} - The fixture providing a `BufferRepository` instance.
    :param tmp_path {Path} - A temporary directory path provided by `pytest`.
    """

    file_path = tmp_path / "test_file"
    file_path.touch()

    prepare_cut_cmd = PrepareCutCommand(empty_transfer_buffer, temp_buffer_repo)
    prepare_cut_cmd.prepare([str(file_path)])


    assert empty_transfer_buffer.default_operation.transfer_type == TransferType.CUT
