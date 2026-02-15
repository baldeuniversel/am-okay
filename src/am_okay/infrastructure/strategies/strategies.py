
import os
import shutil
import threading
from pathlib import Path
from abc import ABC, abstractmethod

from am_okay.infrastructure.observers.observers import ProgressObserver
from am_okay.utils.cancellation_utils import CancellationToken
from am_okay.domain.transfer_operation import TransferType



class TransferStrategy(ABC):
    """
    @overview An abstract strategy interface for executing transfer operations.
    This class contains some implemented methods.

    General responsibilities:
      - Define a common interface for different transfer behaviors (`copy/COPY` or `cut/CUT`)
      - Ensure progress reporting and cancellation support
    """


    @abstractmethod
    def execute(self, sources: list[Path], destination: Path, progress_observer: ProgressObserver, cancel_token: CancellationToken) -> None:
        """
        @overview A method to execute the transfer operation on the given sources.

        :param sources {list[Path]} - The list of files or directories to transfer.
        :param destination {Path} - The target directory for the transfer.
        :param progress_observer {ProgressObserver} - The observer to track transfer progress.
        :param cancel_token {CancellationToken} - The token that allows canceling the transfer.
        """

        pass



    def compute_and_set_total(self, src: Path, progress_observer: ProgressObserver) -> None:
        """
        @overview A method to compute the total size of a directory and update the progress bar.

        :param src {Path} - The source directory to compute the size of.
        :param progress_observer {ProgressObserver} - The observer used to update the total size.
        """

        total = self.compute_total_size(src)
        progress_observer.set_total(total)



    @staticmethod
    def compute_total_size(path: Path) -> int:
        """
        @overview A method to compute the total size (in bytes) of a file or directory.
        For directories, the size is computed recursively as the sum of all contained files.

        :param path {Path} - The file or directory to compute the size of.

        :return {int} - The total size in bytes.
        """

        if path.is_file():
            return path.stat().st_size


        return sum(target_file_or_dir.stat().st_size for target_file_or_dir in path.rglob("*") if target_file_or_dir.is_file())



class CopyStrategy(TransferStrategy):
    """
    @overview A strategy class for copying files and directories with adaptive progress reporting.

    General responsibilities:
      - Copy files or directories recursively
      - Report progress per chunk to the observer
      - Calculate total size of directories asynchronously
      - Support cancellation during transfer
    """


    __CHUNK_SIZE = 1024 * 1024  # 1 MB per chunk



    def execute(self, sources: list[Path], destination: Path, progress_observer: ProgressObserver, cancel_token: CancellationToken) -> None:
        """
        @overview A method to execute the transfer operation on the given sources.

        :param sources {list[Path]} - The list of files or directories to transfer.
        :param destination {Path} - The target directory for the transfer.
        :param progress_observer {ProgressObserver} - The observer to track transfer progress.
        :param cancel_token {CancellationToken} - The token that allows canceling the transfer.
        """

        #
        count_total_paths = len(sources)
        count_current_path = 1

        
        for src in sources:

            cancel_token.check_cancel()
            target = destination / src.name


            # Start progress bar immediately with unknown total for directories
            progress_observer.on_start(src, target, count_current_path, count_total_paths, total_size=1 if src.is_dir() else src.stat().st_size)


            # If directory, compute total size in background thread
            if src.is_dir():

                thread = threading.Thread(
                    target=super().compute_and_set_total, args=(src, progress_observer), daemon=True
                )

                thread.start()

                self._copy_dir(src, target, progress_observer, cancel_token)

            else:
                self._copy_file(src, target, progress_observer, cancel_token)


            progress_observer.on_complete()


            #
            count_current_path += 1



    def _copy_file(self, src_file: Path, dst_file: Path, progress_observer: ProgressObserver, cancel_token: CancellationToken) -> None:
        """
        @overview A method to copy a single file in chunks (the progress will be reported - observer).

        :param src_file {Path} - The source file.
        :param dst_file {Path} - The destination file.
        :param progress_observer {ProgressObserver} - An observer to report progress.
        :param cancel_token {CancellationToken} - The cancellation `token`.
        """

        dst_file.parent.mkdir(parents=True, exist_ok=True)


        with open(src_file, "rb") as file_src, open(dst_file, "wb") as file_dst:

            while chunk := file_src.read(self.__CHUNK_SIZE):
                cancel_token.check_cancel()
                file_dst.write(chunk)
                progress_observer.update(len(chunk))



    def _copy_dir(self, src_dir: Path, dst_dir: Path, progress_observer: ProgressObserver, cancel_token: CancellationToken) -> None:
        """
        @overview  A method to recursively copy a directory, preserving structure (the progress will be reported).

        :param src_dir {Path} - The source directory.
        :param dst_dir {Path} - The destination directory.
        :param progress_observer {ProgressObserver} - An observer for progress updates.
        :param cancel_token {CancellationToken} - The cancellation `token`.
        """

        dst_dir.mkdir(parents=True, exist_ok=True)

        for item in src_dir.iterdir():

            cancel_token.check_cancel()
            target = dst_dir / item.name


            if item.is_dir():
                self._copy_dir(item, target, progress_observer, cancel_token)

            else:
                self._copy_file(item, target, progress_observer, cancel_token)



class CutStrategy(TransferStrategy):
    """
    @overview A strategy class for moving (cutting) files and directories with adaptive progress reporting.

    General responsibilities:
      - Move files or directories recursively
      - Use fast move if source and destination are on the same partition (the progress will be reported)
      - Perform chunked moves with a progress bar for cross-partition transfers
      - Support cancellation
    """


    __CHUNK_SIZE = 1024 * 1024  # 1 MB per chunk



    def execute(self, sources: list[Path], destination: Path, progress_observer: ProgressObserver, cancel_token: CancellationToken) -> None:
        """
        @overview A method to execute the transfer operation on the given sources.

        :param sources {list[Path]} - The list of files or directories to transfer.
        :param destination {Path} - The target directory for the transfer.
        :param progress_observer {ProgressObserver} - The observer to track transfer progress.
        :param cancel_token {CancellationToken} - The token that allows canceling the transfer.
        """

        #
        count_total_paths = len(sources)
        count_current_path = 1


        for src in sources:

            cancel_token.check_cancel()
            target = destination / src.name


            # Start progress bar with unknown total initially
            progress_observer.on_start(src, target, count_current_path, count_total_paths, total_size=1 if src.is_dir() else src.stat().st_size)


            # Compute total size in background for directories
            if src.is_dir():
                thread = threading.Thread(target=super().compute_and_set_total, args=(src, progress_observer), daemon=True)
                thread.start()


            # Fast move if same partition
            if self.same_partition(src, destination):
                shutil.move(str(src), str(target))

            else:

                # Chunked move with progress updates
                if src.is_dir():
                    self._move_dir(src, target, progress_observer, cancel_token)

                else:
                    self._move_file(src, target, progress_observer, cancel_token)


            # Complete progress bar (set to 100% if still in progress)
            progress_observer.on_complete()


            #
            count_current_path += 1



    @staticmethod
    def same_partition(src: Path, dst: Path) -> bool:
        """
        @overview A method to check if source and destination are on the same filesystem/partition.

        :param src {Path} - The source path.
        :param dst {Path} - The destination path

        :return {bool} - `True` if same partition, `False` otherwise.
        """

        return os.stat(src.parent).st_dev == os.stat(dst.parent).st_dev



    def _move_file(self, src_file: Path, dst_file: Path, progress_observer: ProgressObserver, cancel_token: CancellationToken) -> None:
        """
        @overview A method to move a single file in chunks with progress updates.

        :param src_file {Path} - The source file.
        :param dst_file {Path} - The destination file.
        :param progress_observer {ProgressObserver} - An observer for progress.
        :param cancel_token {CancellationToken} - The cancellation token.
        """

        dst_file.parent.mkdir(parents=True, exist_ok=True)


        with open(src_file, "rb") as file_src, open(dst_file, "wb") as file_dst:

            while chunk := file_src.read(self.__CHUNK_SIZE):
                cancel_token.check_cancel()
                file_dst.write(chunk)
                progress_observer.update(len(chunk))


        src_file.unlink()  # Remove original



    def _move_dir(self, src_dir: Path, dst_dir: Path, progress_observer: ProgressObserver, cancel_token: CancellationToken) -> None:
        """
        @overview A method to recursively move a directory, preserving structure (the progress will be reported).

        :param src_dir {Path} - The source directory.
        :param dst_dir {Path} - The destination directory.
        :param progress_observer {ProgressObserver} - An observer for progress.
        :param cancel_token {CancellationToken} - The cancellation token.
        """

        dst_dir.mkdir(parents=True, exist_ok=True)


        for item in src_dir.iterdir():

            cancel_token.check_cancel()
            target_item = dst_dir / item.name

            if item.is_dir():
                self._move_dir(item, target_item, progress_observer, cancel_token)

            else:
                self._move_file(item, target_item, progress_observer, cancel_token)


        src_dir.rmdir()  # Remove empty folder



class TransferStrategyFactory:
    """
    @overview A factory class for creating transfer strategies based on the transfer type.

    General responsibilities:
      - Return a strategy instance (`CopyStrategy` or `CutStrategy`)
      - Encapsulate strategy creation logic
    """


    @staticmethod
    def create(transfer_type: TransferType) -> TransferStrategy:
        """
        @overview A method to return an appropriate strategy instance based on transfer type.

        :param transfer_type {TransferType} - The transfer type.
        
        :return {TransferStrategy} - A strategy instance.
        """

        if transfer_type == TransferType.COPY:
            return CopyStrategy()
        

        return CutStrategy()
