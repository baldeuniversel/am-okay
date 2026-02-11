
"""
@overview Command-line interface for the `am-okay` program tool.

General responsibilities:
  - Parse CLI arguments
  - Support slot-based operations and default operations
  - Delegate to preparation, paste, stat, and reset commands
  - Handle immediate preparation + execution
"""

import sys
import argparse
from pathlib import Path
from typing import List
import random

from am_okay.infrastructure.repository.buffer_repository import BufferRepository
from am_okay.application.prepare_commands import (
    PrepareCopyCommand, PrepareCutCommand, 
    PrepareTransferCommand
)
from am_okay.application.execute_commands import PasteCommand, StatCommand
from am_okay.infrastructure.observers.observers import TqdmProgressObserver
from am_okay.utils.path_utils import normalize_paths
from am_okay.utils.path_stat_utils import PathStat
from am_okay.utils.wait_animation_utils import (
    CircleAnimation, SpinnerAnimation, 
    IndeterminateBarAnimation
)



###
### Helper functions
###
def parse_slot_arg(slot_arg: str) -> list[int | str]:
    """
    @overview A function to parse a `--slot` CLI argument string into a list of integer slot indices
    or the special value "all".

    :param slot_arg {str} - The raw slot argument can be a single number, comma-separated, or range (e.g., 0-2).

    :return {List[int | str]} - The list of slot indices or ["all"].

    :raises {ValueError} - An exception to raise when "all" is combined with explicit slot indices.
    """

    slots: list[int | str] = []

    parts = [part_arg.strip().lower() for part_arg in slot_arg.split(",")]

    # Reject "all" combined with other clues
    if "all" in parts and len(parts) > 1:
        raise ValueError("❌  Invalid usage -> `all` cannot be combined with explicit slot indices")


    for part in parts:

        if part == "all":
            slots.append("all")

        elif "-" in part:

            start_str, end_str = part.split("-", 1)

            if not start_str.isdigit() or not end_str.isdigit():
                raise ValueError(f"❌  Invalid slot range -> '{part}' must be integers, e.g., 0-2")
            
            start, end = int(start_str), int(end_str)

            if start > end:
                raise ValueError(f"❌  Invalid slot range -> start ({start}) `gt` end ({end})")
            
            slots.extend(range(start, end + 1))

        else:

            if not part.isdigit():
                raise ValueError(f"❌  Invalid slot index -> '{part}' must be a non-negative integer")
            
            slots.append(int(part))


    return slots



def iter_slots(slots, transfer_buffer) -> List[int]:
    """
    @overview A helper function that resolves slot indices to iterate over,
    handling the special `all` keyword.

    General responsibilities:
      - Validate slot arguments consistency
      - Expand the special `all` keyword into actual slot indices
      - Return a clean iterable of slot indices to be processed by commands

    @param slots {List[int | str]} - A list of slot indices or the special value `"all"`.
           Examples:
             - [0]
             - [1, 2, 3]
             - ["all"]

    @param transfer_buffer {TransferBuffer} - The transfer buffer containing
           all prepared slot-based transfer operations.

    @return {List[int]} - A list of slot indices to iterate over.

    @raises {ValueError} - Raised when `"all"` is combined with explicit slot
            indices (e.g. `["all", 1]`), which is considered invalid usage.
    """

    if "all" in slots and len(slots) > 1:
        raise ValueError("`all` cannot be combined with explicit slot indices")

    if "all" in slots:
        return sorted(transfer_buffer.slot_operations.keys())


    return slots



###
### CLI execution
###

def main():
    """
    @overview The entry point for the `am-okay` program.
    """

    parser = argparse.ArgumentParser(
        description="`am-okay` CLI - Copy/Cut files and directories with progress and slots"
    )

    # Slot argument
    parser.add_argument("--slot", type=str, help="Slot index or range for operations")

    #
    parser.add_argument("--paste", type=str, help="Execute prepared operation(s) to destination")

    # Operation flags
    parser.add_argument("--copy", action="store_true", help="Prepare a copy operation")
    parser.add_argument("--cut", action="store_true", help="Prepare a cut operation")
    parser.add_argument("--stat", action="store_true", help="Display prepared operation(s)")
    parser.add_argument("--reset", action="store_true", help="Reset prepared operation(s)")
    parser.add_argument("--info", action="store_true", help="Display filesystem information about files or directories")

    # Files/dirs for preparation
    parser.add_argument("paths", nargs="*", help="Source files or directories for prepare operations")


    args = parser.parse_args()


    # List of animation classes
    animation_classes = [CircleAnimation, SpinnerAnimation, IndeterminateBarAnimation]

    # Random selection of a class
    choice_animation_class = random.choice(animation_classes)


    # Exclude some scenarios
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if args.reset and args.paths:
        print("\n ❌  Invalid usage \n"
            "       `--reset` does not accept any argument. \n\n"
            "✅     Use cases: \n"
            "         am-okay --reset \n"
            "         am-okay --slot all --reset \n"
            "         am-okay --slot 0 --reset"    
        )
        
        sys.exit(1)

    if args.stat and args.paths:
        print("\n ❌  Invalid usage \n"
            "       `--stat` does not accept any argument. \n\n"
            "✅     Use cases: \n"
            "         am-okay --stat \n"
            "         am-okay --slot all --stat \n"
            "         am-okay --slot 0 --stat"
        )
        
        sys.exit(1)

    if args.info and not args.paths:
        print("\n ❌  Invalid usage \n"
            "       `--info` requires at least one file or directory path. \n\n"
            "✅     Use cases: \n"
            "         am-okay --info file1.txt dirA \n"
            "         am-okay --info Downloads"
        )
        sys.exit(1)

    if args.info and (args.stat or args.copy or args.cut or args.paste or args.reset):
        print("\n ❌  Invalid usage \n"
            "       `--info` cannot be combined with other operation flags."
        )
        sys.exit(1)


    # Initialize repository, buffer, path stat ...
    repo_path = Path.home() / ".am-okay" / "am_okay_buffer_repository.json"
    buffer_repository = BufferRepository(repo_path)
    transfer_buffer = buffer_repository.load()
    progress_observer = TqdmProgressObserver()
    path_stat = PathStat(
        animation=choice_animation_class(message="Calculating size")
    )


    # Prepare commands
    prepare_copy = PrepareCopyCommand(transfer_buffer, buffer_repository)
    prepare_cut = PrepareCutCommand(transfer_buffer, buffer_repository)
    paste_cmd = PasteCommand(transfer_buffer, buffer_repository, progress_observer)
    stat_cmd = StatCommand(transfer_buffer)


    # Determine slots
    slots: List[int | str] = []

    try:
        if args.slot:
            slots = parse_slot_arg(args.slot)

    except ValueError as err:
        print(f"\n{err}")

        sys.exit(1)


    try:

        # Handle reset
        if args.reset:

            if args.slot:

                # Slot-based reset
                for slot in iter_slots(slots, transfer_buffer):
                    transfer_buffer.clear_slot_operation_at(slot)

                buffer_repository.save(transfer_buffer)
                print("\nSlot operations reset  ✅")

            else:

                # Default operation reset
                transfer_buffer.clear_default_operation()
                buffer_repository.save(transfer_buffer)

                print("\nDefault operation reset  ✅")


            sys.exit(0)


        # Handle info
        if args.info:

            try:
                paths = normalize_paths(args.paths)

            except Exception as err:
                print(err)
                sys.exit(1)

            for path in paths:

                info = path_stat.stat(path)

                print(f"\n📄 \033[1;032mPath information\033[0m")

                for key, value in info.items():
                    print(f"  \033[1;036m{key:<16}\033[0m: \033[1;037m{value}\033[0m")

            sys.exit(0)


        # Handle prepare operations
        if args.copy or args.cut:

            if not args.paths:
                print("\nNo source paths provided for prepare operation  🧐")

                sys.exit(1)

            try:
                paths = normalize_paths(args.paths)

            except Exception as err:
                print(err)

                sys.exit(1)


            #
            prepare: PrepareTransferCommand = (
                prepare_copy if args.copy else prepare_cut
            )


            if args.slot:

                if len(slots) > 1:
                    print("\n ❌  Invalid usage \n"
                        "       Prepare operations (--copy / --cut) only support `ONE` slot at a time. \n\n"
                        "✅     Use cases: \n"
                        "         am-okay --slot 0 --copy file1.txt dirA \n"
                        "         am-okay --slot 0 --cut file23.txt dirW"
                    )

                    sys.exit(1)


                # Slot-based preparation
                for slot in iter_slots(slots, transfer_buffer):
                    prepare.prepare([str(the_current_path) for the_current_path in paths], slot)

                    print(f"\nPrepared {'COPY' if args.copy else 'CUT'} operation for slot {slot}  ✅")

            else:

                # Default preparation
                prepare.prepare([str(p) for p in paths])

                print(f"\nPrepared default {'COPY' if args.copy else 'CUT'} operation  ✅")


        # Handle paste
        if args.paste:
            dest = Path(args.paste).expanduser().resolve()

            if args.slot:

                for slot in iter_slots(slots, transfer_buffer):

                    try:
                        paste_cmd.execute_slot_at(slot, dest)

                    except Exception as err:
                        print(f"\nSlot[ {slot} ] failed  ❌", err)


            else:
                paste_cmd.execute_default(dest)


        # Handle stat
        if args.stat:

            if args.slot:

                resolved_slots = iter_slots(slots, transfer_buffer)

                if not resolved_slots:
                    print("\nNo prepared operations found in any slot  🧐")

                    sys.exit(0)

                for slot in resolved_slots:
                    stat_cmd.execute_slot_at(slot)
  
            else:
                stat_cmd.execute_default()

    except KeyboardInterrupt:
        print("\n ⚠️  Operation interrupted by the user  🔌")

    except Exception as err:
        print(err)



if __name__ == "__main__":
    main()
