
import pytest
from pathlib import Path

from am_okay.domain.transfer_buffer import TransferBuffer
from am_okay.infrastructure.repository.buffer_repository import BufferRepository
from am_okay.infrastructure.observers.observers import TqdmProgressObserver
from am_okay.utils.cancellation_utils import CancellationToken



@pytest.fixture
def temp_buffer_repo(tmp_path) -> BufferRepository:
    """
    @overview A fixture to provide a temporary `BufferRepository` for testing.

    :param tmp_path {Path} - The temporary directory path provided by pytest.

    :return {BufferRepository} - A `BufferRepository` instance with a temporary JSON file.
    """

    repo_path:Path = tmp_path / "test_buffer.json"


    return BufferRepository(repo_path)



@pytest.fixture
def empty_transfer_buffer() -> TransferBuffer:
    """
    @overview A fixture to provide an empty `TransferBuffer`.

    :return {TransferBuffer} - An empty `TransferBuffer` instance.
    """

    return TransferBuffer()



@pytest.fixture
def progress_observer() -> TqdmProgressObserver:
    """
    @overview A fixture to provide a `ProgressObserver` for testing.

    :return {TqdmProgressObserver} - A `TqdmProgressObserver` instance.
    """

    return TqdmProgressObserver()



@pytest.fixture
def cancellation_token() -> CancellationToken:
    """
    @overview A fixture to provide a `CancellationToken` instance for testing.

    :return {CancellationToken} - A `CancellationToken` instance.
    """

    return CancellationToken()



@pytest.fixture
def mock_store_structure(tmp_path) -> Path:
    """
    @overview A fixture to create a mock 'store' directory structure for testing.

    :param tmp_path {Path} - The temporary directory path provided by pytest.

    :return {Path} - A path to the 'store' directory.
    """

    store_dir:Path = tmp_path / "store"
    aside_dir:Path = store_dir / "aside"
    aside_dir.mkdir(parents=True)


    # Create mock files
    (aside_dir / "file_a").touch()
    (aside_dir / "file_b").touch()
    (aside_dir / "file_c").touch()
    (aside_dir / "ubuntu-20.04.6-desktop-amd64.iso").touch()


    return store_dir
