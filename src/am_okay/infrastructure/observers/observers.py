
from pathlib import Path
from abc import ABC, abstractmethod
from tqdm import tqdm

from am_okay.utils.cli_utils import get_terminal_width, format_transfer_line



class ProgressObserver(ABC):
    """
    @overview An observer interface for monitoring transfer progress.
    """


    @abstractmethod
    def on_start(self, source: Path, destination: Path, total_size: int | None = None) -> None:
        """
        @overview A method to call when a transfer starts.

        :param source {Path} - The source file or directory.
        :param {Path} destination - Target destination path.
        :param total_size {int | None} - The total size in bytes.
        """

        pass



    @abstractmethod
    def set_total(self, total_size: int) -> None:
        """
        @overview A method to set or update the total size of the transfer for streaming directories.

        :param total_size {int} - The total size in bytes.
        """



    @abstractmethod
    def update(self, chunk_size: int) -> None:
        """
        @overview A method to increment the progress bar by chunk size.

        :param chunk_size {int} - The number of bytes processed.
        """

        pass



    @abstractmethod
    def on_complete(self) -> None:
        """
        @overview A method to call when a transfer completes.
        
        @details This method ensures the progress bar reaches `100%` before closing.
        This guarantees correctness even for fast moves on the same disk.
        """

        pass



class TqdmProgressObserver(ProgressObserver):
    """
    @overview A `observer` class, displaying a single `tqdm` progress bar per source.

    General responsibilities:
      - Initialize a progress bar at start of a transfer
      - Update progress for each chunk
      - Dynamically update total size for directories
      - Close the bar on completion
    """


    def on_start(self, source: Path, destination: Path, total_size: int | None = None) -> None:
        """
        @overview A method to call when a transfer starts.

        :param source {Path} - The source file or directory.
        :param {Path} destination - Target destination path.
        :param total_size {int | None} - The total size in bytes.
        """

        terminal_width = get_terminal_width()
        header_progress_bar = format_transfer_line(source, destination, terminal_width)

        tqdm.write("")
        tqdm.write(header_progress_bar)

        
        self._progress_bar = tqdm(total=total_size or 1, unit="B", unit_scale=True, 
            unit_divisor=1024, leave=True, desc="", ncols=terminal_width,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        )



    def set_total(self, total_size: int) -> None:
        """
        @overview A method to set or update the total size of the transfer for streaming directories.

        :param total_size {int} - The total size in bytes.
        """

        if self._progress_bar:
            self._progress_bar.total = total_size
            self._progress_bar.refresh()



    def update(self, chunk_size: int) -> None:
        """
        @overview A method to increment the progress bar by chunk size.

        :param chunk_size {int} - The number of bytes processed.
        """

        if self._progress_bar:
            self._progress_bar.update(chunk_size)



    def finish(self) -> None:
        """
        @overview A method to close the progress bar when the transfer completes.
        """

        if self._progress_bar:
            self._progress_bar.close()
            #self._progress_bar = None



    def on_complete(self) -> None:
        """
        @overview A method to call when a transfer completes.
        
        @details This method ensures the progress bar reaches `100%` before closing.
        This guarantees correctness even for fast moves on the same disk.
        """

        if self._progress_bar:

            # Force progress bar to 100%
            if (self._progress_bar.n) < (self._progress_bar.total or 0):
                self._progress_bar.update((self._progress_bar.total or 0) - self._progress_bar.n)

            self.finish()
