
from typing import Dict

from am_okay.domain.transfer_operation import TransferOperation



class TransferBuffer:
    """
    @overview A class that manages prepared transfer operations, either in slot-based mode or in default mode.
    This class provides CRUD functionality for the buffer repository, applying transfer operation instructions as needed.

    General responsibilities:
      - Initialize a transfer operation using transfer operation instructions. The buffer repository 
        persists the operation via the transfer buffer (which linked to transfer operation instructions).
      - Update the prepared operations for slot-based mode (via transfer operation instructions).
      - Update the prepared operations for non-slot-based mode (via transfer operation instructions).
      - Ensure only one operation type (`COPY` or `CUT`) per slot (via transfer operation instructions).
      - Ensure only one operation (`COPY` or `CUT`) for the non slot-based mode (via transfer operation instructions).
      - Provide methods to indirectly perform CRUD operations (via transfer operation instructions) on the 
        buffer repository (-> using the transfer buffer to perform updates on the buffer repository).
    """


    def __init__(self):
        """
        @overview A magic method that initializes an empty transfer buffer.
        """

        self.__slot_operations: Dict[int, TransferOperation] = {} # A dictionary mapping slot indices (one index for one operation)
        self.__default_operation: TransferOperation | None = None # The default transfer operation (non slot-based mode)



    @property
    def slot_operations(self) -> Dict[int, TransferOperation] | Dict:
        """
        @overview A property method to get all slots (slot-based mode) from the buffer repository.

        :return {Dict[int, TransferOperation] | None} - A mapping of slot indices to their prepared operations, or `None`.
        """

        return self.__slot_operations



    @property
    def default_operation(self) -> TransferOperation | None:
        """
        @overview A property method to get the default prepared operation from the buffer repository.

        :return {TransferOperation | None} - The default prepared operation (non slot-based mode), or `None`.
        """

        return self.__default_operation



    def set_slot_operation_at(self, index: int, transfer_operation: TransferOperation) -> None:
        """
        @overview A method that updates an operation at the specified slot index (slot-based mode) in the buffer repository.
        
        :param index {int} - The index of the slot in the buffer repository.
        :param transfer_operation {TransferOperation} - The operation (transfer type, source paths - **kargs).

        @flag The method will overwrite any existing prepared operation at the specified slot index.
        """

        # Update the prepared operation at the specified slot index
        self.__slot_operations[index] = transfer_operation



    def set_default_operation(self, transfer_operation: TransferOperation) -> None:
        """
        @overview A method that updates a default operation (non slot-based mode) in the buffer repository.

        :param transfer_operation {TransferOperation} - The operation (transfer type, source paths - **kargs).

        @flag The method will overwrite any existing default prepared operation.
        """

        # Update the prepared operation (non slot-based mode)
        self.__default_operation = transfer_operation



    def get_slot_operation_at(self, index: int) -> TransferOperation | None:
        """
        @overview A method that allows retrieving the prepared operation at a specific slot index from the buffer repository.

        :param index {int} - The index of the slot in the buffer repository.

        :return {TransferOperation | None} - The prepared operation at the specific slot index, or `None`.
        """

        return self.__slot_operations.get(index) if self.__slot_operations.get(index) else None



    def clear_slot_operation_at(self, index: int) -> None:
        """
        @overview A method that clears a slot index along with its linked operation in the buffer repository.

        :param index {int} - The index of the slot index to clear in the buffer repository.
        """

        if self.__slot_operations:
            self.__slot_operations.pop(index, None)
    


    def clear_all_slot_operations(self) -> None:
        """
        @overview A method to clear all prepared operations stored in slot-based mode in the buffer repository.
        After this call, the slot operations dictionary will be empty.
        """

        if self.__slot_operations:
            self.__slot_operations.clear()



    def clear_default_operation(self) -> None:
        """
        @overview A method that clears a default operation in the buffer repository.
        """

        self.__default_operation = None
