
from pathlib import Path
from typing import List, Callable

from am_okay.domain.transfer_buffer import TransferBuffer
from am_okay.domain.transfer_operation import TransferOperation, TransferType
from am_okay.infrastructure.repository.buffer_repository import BufferRepository
from am_okay.utils.path_utils import normalize_paths
from am_okay.domain.validators import validate_source_path



class PrepareTransferCommand:
    """
    @overview A base class for preparing transfer operations.

    General responsibilities:
      - Normalize input source paths
      - Create a prepared transfer operation
      - Prepare transfer buffer operations in either slot-based mode or default mode
      - Persist the prepared transfer buffer state using a repository (the buffer repository)
      - Validate paths using a mandatory validator
    """


    def __init__(self, transfer_buffer: TransferBuffer, buffer_repository: BufferRepository, 
        transfer_type: TransferType,
        validator_src_path: Callable[[List[Path]], None]
    ):
        """
        @overview A magic method that initializes a prepared transfer command.

        :param transfer_buffer {TransferBuffer} - The transfer buffer that manages prepared transfer operations, 
               either in slot-based mode or in the default mode.
        :param buffer_repository {BufferRepository} - The buffer repository that manages the persistence of the 
               transfer buffer. It provides methods like `load` and `save`, using `JSON` format for storage.
        :param transfer_type {TransferType} - The transfer type (`COPY` or `CUT`).
        :param validator_src_path {Callable[[List[Path]], None]} - A required `callable` that validates a 
               list of paths (mandatory `function`).
        """

        self.__transfer_buffer = transfer_buffer
        self.__buffer_repository = buffer_repository
        self.__transfer_type = transfer_type
        self.__validator_source_path = validator_src_path



    def prepare(self, paths: List[str], index: int | None = None) -> None:
        """
        @overview A method that prepares a transfer operation and stores it in the buffer repository (through the transfer buffer).

        :param paths {List[str]} - The list of source paths to be used in preparing the transfer operation.
        :param index {int} - The index of the slot to be used in preparing the transfer operation. If `None` the 
               default mode is used. 

        :raises {ValidatorMissingError | FileNotFoundError} - Exceptions that may be raised.
        """

        # Normalize paths
        normalized_paths: List[Path] = normalize_paths(paths)
        

        # Validate paths if validator is provided
        if self.__validator_source_path is not None:
            self.__validator_source_path(normalized_paths)

        else:
            raise ValidatorMissingError("\nA validator `callback` must be provided to validate source paths  🧐")


        # Create transfer operation
        transfer_operation = TransferOperation(
            self.__transfer_type,
            [str(the_path) for the_path in normalized_paths]
        )


        # Prepare the desired operation 
        if index is None:
            self.__transfer_buffer.set_default_operation(transfer_operation)

        else:
            self.__transfer_buffer.set_slot_operation_at(index, transfer_operation)


        # Update the buffer repository (through the transfer buffer)
        self.__buffer_repository.save(self.__transfer_buffer)



class PrepareCopyCommand(PrepareTransferCommand):
    """
    @overview A class for preparing a `COPY` transfer operation (see the base class for further details).
    """


    def __init__(self, transfer_buffer: TransferBuffer, buffer_repository: BufferRepository):
        """
        @overview See the parent class for further details.
        """

        super().__init__(
            transfer_type=TransferType.COPY,
            transfer_buffer=transfer_buffer,
            buffer_repository=buffer_repository,
            validator_src_path=lambda paths: validate_source_path(paths, transfer_type=TransferType.COPY)
        )



class PrepareCutCommand(PrepareTransferCommand):
    """
    @overview A class for preparing a `CUT` transfer operation (see the base class for further details).
    """


    def __init__(self, transfer_buffer: TransferBuffer, buffer_repository: BufferRepository):
        """
        @overview See the parent class for further details.
        """

        super().__init__(
            transfer_type=TransferType.CUT,
            transfer_buffer=transfer_buffer,
            buffer_repository=buffer_repository,
            validator_src_path=lambda paths: validate_source_path(paths, transfer_type=TransferType.CUT)
        )



class ValidatorMissingError(Exception):
    """
    @overview A class of type `Exception` raised when a validator `callback` is required but not provided.
    """

    pass
