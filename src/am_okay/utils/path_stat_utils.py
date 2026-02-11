
import stat
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import mimetypes
import pwd
import grp

from am_okay.utils.wait_animation_utils import WaitAnimation



class PathStat:
    """
    @overview A utility class that provides filesystem statistics
    for files and directories.

    General responsibilities:
      - Inspect file or directory metadata
      - Compute recursive directory size
      - Format sizes using human-readable units
      - Provide optional animation during computation
    """


    __UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]



    def __init__(self, animation: WaitAnimation | None = None):
        """
        @overview A magic method that initializes the `PathStat` utility.

        :param animation {WaitAnimation | None} - Optional wait animation
               displayed during size calculation.
        """

        self._animation = animation

    

    def _size_convertor(self, num_bytes: int) -> str:
        """
        @overview A method to convert a size in bytes into a human-readable string.

        @details The conversion is based on a `1024` multiplier and automatically
        selects the most appropriate unit up to petabytes (PiB).

        :param num_bytes {int} - The size expressed in bytes.

        :return {str} - A human-readable size representation.
        """

        size = float(num_bytes)


        for unit in self.__UNITS:

            if size < 1024:
                return f"{size:.2f} {unit}"
            
            size /= 1024


        return f"{size:.2f} PiB"



    def _get_dir_size(self, path: Path) -> tuple[int, bool]:
        """
        @overview A method to recursively calculate the total size of a directory.

        @details Only regular files are counted. Inaccessible files are silently
        ignored to ensure robustness.

        :param path {Path} - The directory path.

        :return {tuple[int, bool]} where:
                - int: The total directory size in bytes.
                - bool: The computing sate, `True` if the computation completed 
                  without errors, `False` otherwise.
        """

        total = 0
        flag_no_error = True


        for file in path.rglob("*"):

            if file.is_file():

                try:
                    total += file.stat().st_size

                except OSError:
                    flag_no_error = False


        return (total, flag_no_error)



    def stat(self, path: str | Path) -> Dict[str, str | int | datetime]:
        """
        @overview A method that retrieves filesystem statistics for a file or directory.

        :param path {str | Path} - The path to the file or directory.

        :return {Dict[str, str | int]} - A dictionary containing filesystem statistics for the given path.

        :raises {FileNotFoundError} - An exception to raise if the `path` does not exist.
        """

        target_path = Path(path)


        if not target_path.exists():
            raise FileNotFoundError(f"\nPath does not exist: {path}  🧐")


        if self._animation:
            self._animation.start()


        try:

            stat_path = target_path.stat()
      
            try:

                if target_path.is_file():
                    size_bytes = stat_path.st_size
                    flag_size_computing = True

                else:
                    size_bytes, flag_size_computing = self._get_dir_size(target_path)

            except (OSError, Exception):
                size_bytes = 0
                flag_size_computing = False


            # Determine mimetype for files
            mime_type: Optional[str] = None

            if target_path.is_file():
                mime_type, _ = mimetypes.guess_type(str(target_path))


            owner_human_readable = pwd.getpwuid(stat_path.st_uid).pw_name
            group_human_readable = grp.getgrgid(stat_path.st_gid).gr_name
            owner_uid = pwd.getpwuid(stat_path.st_uid).pw_uid
            group_gid = grp.getgrgid(stat_path.st_gid).gr_gid

        finally:
            if self._animation:
                self._animation.stop()


        info_path_part_1: Dict[str, str | int | datetime] = {
            "name": target_path.name,
            "type": "directory" if target_path.is_dir() else "file",
        }

        # Add mimetype only for files
        if target_path.is_file():
            info_path_part_1["mimetype"] = mime_type or "Unknown"

        info_path_part_2: Dict[str, str | int | datetime] = {
            "size": self._size_convertor(size_bytes),
            "size_ok": "✅" if flag_size_computing else "⚠️",
            "permissions": stat.filemode(stat_path.st_mode),
            "owner_name": owner_human_readable,
            "group_name": group_human_readable,
            "owner_uid": owner_uid,
            "group_gid": group_gid,
            "created": datetime.fromtimestamp(stat_path.st_ctime),
            "modified": datetime.fromtimestamp(stat_path.st_mtime),
            "absolute_path": str(target_path.resolve()),
        }

        info_path: Dict[str, str | int | datetime] = info_path_part_1
        info_path.update(info_path_part_2)


        return info_path
