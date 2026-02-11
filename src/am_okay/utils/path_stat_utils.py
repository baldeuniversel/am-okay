
import sys
import stat
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

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



    @staticmethod
    def get_path_owner_and_group(path: Path) -> Dict[str, str | int | None]:
        """
        @overview A static method to retrieve the owner and group of a file or directory.

        @details On Linux/macOS, it uses UID/GID to resolve human-readable names.
                On Windows, it uses pywin32's `win32security` module to resolve 
                the owner and group names from the security descriptor.

        :param path {Path} - The file or directory path.

        :return {Dict[str, str | int | None]} - A dictionary containing the owner and group information for the given path.
        """

        target_path = Path(path)


        try:

            stat_path = target_path.stat()


            if sys.platform.startswith("win"):

                ###
                ### Windows
                ###

                try:

                    import win32security # type: ignore


                    security_descriptor = win32security.GetFileSecurity(
                        str(target_path),
                        win32security.OWNER_SECURITY_INFORMATION |
                        win32security.GROUP_SECURITY_INFORMATION
                    )

                    owner_sid = security_descriptor.GetSecurityDescriptorOwner()
                    group_sid = security_descriptor.GetSecurityDescriptorGroup()
                    owner_name, owner_domain, _ = win32security.LookupAccountSid(None, owner_sid)
                    group_name, group_domain, _ = win32security.LookupAccountSid(None, group_sid)


                    return {
                        "owner_name": f"{owner_domain}\\{owner_name}",
                        "group_name": f"{group_domain}\\{group_name}",
                        "owner_uid": None,
                        "group_gid": None,
                    }

                except ImportError:
                    return {
                        "owner_name": "Unknown",
                        "group_name": "Unknown",
                        "owner_uid": None,
                        "group_gid": None,
                    }

            elif sys.platform.startswith(("linux", "darwin")):
                
                ###
                ### Linux / macOS 
                ###

                import pwd
                import grp


                owner_name = pwd.getpwuid(stat_path.st_uid).pw_name
                group_name = grp.getgrgid(stat_path.st_gid).gr_name
                owner_uid = stat_path.st_uid
                group_gid = stat_path.st_gid


                return {
                    "owner_name": owner_name,
                    "group_name": group_name,
                    "owner_uid": owner_uid,
                    "group_gid": group_gid,
                }
            
            else:

                ###
                ### Unsupported OS
                ###

                return {
                    "owner_name": "Unknown",
                    "group_name": "Unknown",
                    "owner_uid": None,
                    "group_gid": None,
                }
            
        except Exception:
            return {
                "owner_name": "Unknown",
                "group_name": "Unknown",
                "owner_uid": None,
                "group_gid": None,
            }



    def stat(self, path: str | Path) -> Dict[str, str | int | datetime | None]:
        """
        @overview A method that retrieves filesystem statistics for a file or directory.

        :param path {str | Path} - The path to the file or directory.

        :return {Dict[str, str | int | datetime | None]} - A dictionary containing filesystem statistics for the given path.

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
                
                try:
                    import magic


                    mime_type = magic.from_file(str(target_path), mime=True)

                except ImportError:
                    import mimetypes


                    # fallback on `mimetypes` if `magic` can not resolve
                    mime_type, _ = mimetypes.guess_type(str(target_path))

            
            owner_path_info = self.get_path_owner_and_group(target_path)

            owner_human_readable = owner_path_info["owner_name"]
            group_human_readable = owner_path_info["group_name"]
            owner_uid = owner_path_info["owner_uid"]
            group_gid = owner_path_info["group_gid"]

        except Exception as error:
            size_bytes = 0
            flag_size_computing = False
            mime_type = None
            owner_human_readable = "Unknown"
            group_human_readable = "Unknown"
            owner_uid = None
            group_gid = None

        finally:
            if self._animation:
                self._animation.stop()

        # Path date (modification, creation)
        try:
            created = datetime.fromtimestamp(stat_path.st_ctime)

        except (OSError, OverflowError, ValueError):
            created = None

        try:
            modified = datetime.fromtimestamp(stat_path.st_mtime)
            
        except (OSError, OverflowError, ValueError):
            modified = None


        info_path_part_1: Dict[str, str | int | datetime | None] = {
            "name": target_path.name,
            "type": "directory" if target_path.is_dir() else "file",
        }

        # Add mimetype only for files
        if target_path.is_file():
            info_path_part_1["mimetype"] = mime_type or "Unknown"

        info_path_part_2: Dict[str, str | int | datetime | None] = {
            "size": self._size_convertor(size_bytes),
            "size_ok": "✅" if flag_size_computing else "⚠️",
            "permissions": stat.filemode(stat_path.st_mode),
            "owner_name": owner_human_readable,
            "group_name": group_human_readable,
            "owner_uid": owner_uid,
            "group_gid": group_gid,
            "created": created,
            "modified": modified,
            "absolute_path": str(target_path.resolve()),
        }

        info_path: Dict[str, str | int | datetime | None] = info_path_part_1
        info_path.update(info_path_part_2)


        return info_path
