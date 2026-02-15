
import shutil
from pathlib import Path



def get_terminal_width(default: int = 80) -> int:
    """
    @overview A function that returns the width of the current terminal in characters (counting).

    :param {int} default -  The fallback width in case terminal size cannot be determined.

    :return {int} - The width of the terminal in characters (counting).
    """

    return shutil.get_terminal_size(fallback=(default, 24)).columns



def truncate_middle(text: str, max_len: int) -> str:
    """
    @overview A function that truncates a string in the middle to fit within a maximum 
    length, inserting '...' if needed.

    :param {str} text - The original string to truncate.
    :param {int} max_len - The max length of the returned string.

    :return {str} - The truncated string with '...' in the middle if exceeded `max_len`.
    """

    if len(text) <= max_len:
        return text

    if max_len < 5:
        return text[:max_len]


    part = (max_len - 3) // 2


    return f"{text[:part]}...{text[-part:]}"



def format_transfer_line(source: Path, destination: Path, width: int, transfer_ratio_between_current_and_total: str) -> str:
    """
    @overview A function that formats a transfer line showing 'source -> destination', 
    truncated to fit terminal width.

    :param {Path} source - The source file or directory.
    :param {Path} destination - The destination file or directory.
    :param {int} width - The max terminal width in characters (counting).
    :param {str} transfer_ratio_between_current_and_total - The ratio between the current 
           transfer position number and the total number of transfers to be completed.

    :return {str} - The formatted line with source and destination truncated as needed.
    """

    arrow = " -> "
    the_transfer_ratio_btw_current_and_total = transfer_ratio_between_current_and_total

    available = width - (len(arrow) + len(the_transfer_ratio_btw_current_and_total))
    half = available // 2

    src = truncate_middle(str(source), half)
    dst = truncate_middle(str(destination), available - len(src))


    return f"{src}{arrow}{dst}"
