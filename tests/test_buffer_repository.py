
from am_okay.infrastructure.repository.buffer_repository import BufferRepository
from am_okay.domain.transfer_buffer import TransferBuffer
from am_okay.domain.transfer_operation import TransferOperation, TransferType



def test_buffer_repository_save_and_load(mock_store_structure, tmp_path):
    """
    @overview Test case validating the saving and loading of a `TransferBuffer` 
    within a realistic file structure.

    :param mock_store_structure {Path} - The path to the mock 'store' directory.
    :param tmp_path {Path} - The temporary directory path provided by `pytest`.
    """

    # Use the file structure created by the fixture
    aside_dir = mock_store_structure / "aside"

    # Create a transfer operation with realistic paths
    transfer_operation = TransferOperation(
        TransferType.COPY,
        [
            str(aside_dir / "file_a"),
            str(aside_dir / "file_b"),
            str(aside_dir / "file_c"),
            str(aside_dir / "ubuntu-20.04.6-desktop-amd64.iso")
        ]
    )

    # Initialize the BufferRepository with a JSON file in tmp_path
    buffer_repository = BufferRepository(tmp_path / "test_buffer.json")
    transfer_buffer = TransferBuffer()


    # Set the default operation
    transfer_buffer.set_default_operation(transfer_operation)


    # Save and load the buffer
    buffer_repository.save(transfer_buffer)
    loaded_buffer = buffer_repository.load()


    # Verify that the operation was correctly saved and loaded
    assert loaded_buffer.default_operation.transfer_type == TransferType.COPY
    assert len(loaded_buffer.default_operation.source_paths) == 4
    assert str(aside_dir / "file_a") in loaded_buffer.default_operation.source_paths
    assert str(aside_dir / "ubuntu-20.04.6-desktop-amd64.iso") in loaded_buffer.default_operation.source_paths
