
from pathlib import Path

from am_okay.infrastructure.strategies.strategies import TransferStrategyFactory
from am_okay.infrastructure.observers.observers import ProgressObserver
from am_okay.utils.cancellation_utils import CancellationToken
from am_okay.infrastructure.repository.buffer_repository import BufferRepository
from am_okay.domain.transfer_buffer import TransferBuffer
from am_okay.domain.validators import validate_destination_dir, validate_source_path



class PasteCommand:
    """
    @overview A class for executing prepared transfer operations from the buffer repository (through the transfer buffer).

    General responsibilities:
      - Execute `COPY` or `CUT` operations
      - Handle slot-specific operations (via indices), or fall back to the default behavior when no slot is specified
      - Notify progress observer
      - Clear `Cut` operations from the buffer after execution
    """


    def __init__(self, transfer_buffer: TransferBuffer, buffer_repository: BufferRepository, progress_observer: ProgressObserver):
        """
        @overview A magic method that initializes a command.

        :param transfer_buffer {TransferBuffer} - The transfer buffer that manages prepared transfer operations, 
               either in slot-based mode or in the default mode.
        :param buffer_repository {BufferRepository} - The buffer repository that manages the persistence of the 
               transfer buffer. It provides methods like `load` and `save`, using `JSON` format for storage.
        :param progress_observer {ProgressObserver} - An observer that tracks and reports the progress of the transfer.
        """

        self.__transfer_buffer = transfer_buffer
        self.__buffer_repository = buffer_repository
        self.__progress_observer = progress_observer



    def execute_slot_at(self, index: int, destination_dir: Path, cancel_token: CancellationToken | None = None) -> None:
        """
        @overview A method that executes a prepared transfer operation stored in a specific slot (by index) in 
        the buffer repository (through the transfer buffer).

        :param index {int} - The index of the slot storing the prepared operation in the buffer 
               repository (through the transfer buffer).
        :param destination_dir {Path} - The target destination directory.
        :param cancel_token {CancellationToken | None} - An optional cancellation `token` 
               used to interrupt the transfer.

        :raises {NoPreparedOperationError} - An exception to raise when a transfer operation is 
        requested but the transfer buffer contains no prepared operation.
        """

        # Ensure that the destination directory exists and is writable
        validate_destination_dir(destination_dir)


        # Retrieve the prepared transfer operation at the given slot index
        transfer_operation = self.__transfer_buffer.get_slot_operation_at(index)
        
        #
        if not transfer_operation:
            raise NoPreparedOperationError(f"\nNo prepared operation for slot {index}  🧐")
        
        # Check permissions for a transfer atomicity (the intent)  
        source_paths:list[Path] = [Path(the_path) for the_path in transfer_operation.source_paths]
        validate_source_path(source_paths, transfer_operation.transfer_type)
        

        # -> More relevant for the test part (pytest)
        token = cancel_token or CancellationToken()


        # Create the appropriate transfer strategy instance based on the operation type (`COPY` or `CUT`)
        transfer_strategy = TransferStrategyFactory.create(transfer_operation.transfer_type)

        # Execute the strategy:
        #   - Convert all source paths to Path objects
        #   - Pass the destination directory
        #   - Provide the progress observer to track transfer progress
        #   - Provide an eventual cancellation token to allow aborting the operation
        transfer_strategy.execute([Path(the_path) for the_path in transfer_operation.source_paths], destination_dir, self.__progress_observer, token)


        if transfer_operation.is_cut_operation():
            self.__transfer_buffer.clear_slot_operation_at(index)


        # Update the buffer repository (through the transfer buffer)
        self.__buffer_repository.save(self.__transfer_buffer)



    def execute_default(self, destination_dir: Path, cancel_token: CancellationToken | None = None) -> None:
        """
        @overview A method that executes a default prepared transfer operation (non slot-based mode) stored in 
        the buffer repository (through the transfer buffer).

        :param {Path} destination_dir - The target directory.

        :raises {NoPreparedOperationError} - An exception to raise when a transfer operation is 
        requested but the transfer buffer contains no prepared operation.
        """

        # Ensure that the destination directory exists and is writable
        validate_destination_dir(destination_dir)


        # Retrieve the prepared transfer operation (non slot-based mode)
        transfer_operation = self.__transfer_buffer.default_operation

        #
        if not transfer_operation:
            raise NoPreparedOperationError("\nNo prepared default operation  🧐")

        # Check permissions for a transfer atomicity (the intent)  
        source_paths:list[Path] = [Path(the_path) for the_path in transfer_operation.source_paths]
        validate_source_path(source_paths, transfer_operation.transfer_type)


        token = cancel_token or CancellationToken()


        # Create the appropriate transfer strategy instance based on the operation type (`COPY` or `CUT`)
        transfer_strategy = TransferStrategyFactory.create(transfer_operation.transfer_type)

        # Execute the strategy
        transfer_strategy.execute([Path(the_path) for the_path in transfer_operation.source_paths], destination_dir, self.__progress_observer, token)


        if transfer_operation.is_cut_operation():
            self.__transfer_buffer.clear_default_operation()


        # Update the buffer repository (through the transfer buffer)
        self.__buffer_repository.save(self.__transfer_buffer)



class StatCommand:
    """
    @overview A class for displaying prepared transfer operations from the buffer repository (through the transfer buffer).

    General responsibilities:
      - Show slot-based or default prepared transfer operations
    """


    def __init__(self, transfer_buffer: TransferBuffer):
        """
        @overview A magic method that initializes a command.

        :param transfer_buffer {TransferBuffer} - The transfer buffer that manages prepared transfer operations, 
               either in slot-based mode or in the default mode.
        """

        self.__transfer_buffer = transfer_buffer



    def execute_slot_at(self, index: int) -> None:
        """
        @overview A method that displays a prepared transfer operation stored in a specific slot (by index) in 
        the buffer repository (through the transfer buffer).

        :param index {int} - The index of the slot whose prepared transfer operation is to be displayed.

        :raises {NoPreparedOperationError} - An exception to raise when a transfer operation is 
        requested but the transfer buffer contains no prepared operation.
        """

        # Retrieve the prepared transfer operation at the given slot index
        transfer_operation = self.__transfer_buffer.get_slot_operation_at(index)

        if not transfer_operation:
            raise NoPreparedOperationError(f"\nNo prepared operation for the slot {index}  🧐")


        print(f"\n\033[1;32m[{index}] {transfer_operation.transfer_type.value.upper()}\033[0m")

        for the_path in transfer_operation.source_paths:
            print(f"  \033[1;36m- {the_path}\033[0m")



    def execute_default(self) -> None:
        """
        @overview A method that displays a default prepared transfer operation (non slot-based mode) stored in 
        the buffer repository (through the transfer buffer).

        :raises {NoPreparedOperationError} - An exception to raise when a transfer operation is 
        requested but the transfer buffer contains no prepared operation.
        """

        # Retrieve the prepared transfer operation (non slot-based mode)
        transfer_operation = self.__transfer_buffer.default_operation

        if not transfer_operation:
            raise NoPreparedOperationError("\nNo default prepared transfer operation  🧐")


        print(f"\n\033[1;32m{transfer_operation.transfer_type.value.upper()}\033[0m")

        for the_path in transfer_operation.source_paths:
            print(f"  \033[1;36m- {the_path}\033[0m")



class NoPreparedOperationError(RuntimeError):
    """
    @overview A class of type `RuntimeError` raised when a transfer operation
    is requested but the transfer buffer contains no prepared operation.
    """

    pass
