
from enum import Enum
from typing import List



class TransferType(Enum):
    """
    @overview A enumeration class describing the type of transfer operation.

    General responsibilities:
      - Represent the type of operation (`COPY` or `CUT`)
    """
    

    COPY = "copy"
    CUT = "cut"



class TransferOperation:
    """
    @overview A class that represents a single transfer operation (`COPY` or `CUT`) with source paths.
    """


    def __init__(self, transfer_type: TransferType, source_paths: List[str]):
        """
        @overview A magic method that initializes a transfer operation.

        :param transfer_type {TransferType} - The `COPY` or `CUT` transfer type.
        :param source_paths {List[str]} - The list of source file/dir paths.
        """

        self.__transfer_type = transfer_type  
        self.__source_paths = source_paths             



    @property
    def transfer_type(self) -> TransferType:
        """
        @overview A property method to get the type of transfer operation.

        :return {TransferType} - The `COPY` or `CUT` transfer type.
        """

        return self.__transfer_type



    @transfer_type.setter
    def transfer_type(self, transfer_type: TransferType) -> None:
        """
        @overview A property method to set the type of transfer operation.

        :param transfer_type {TransferType} - The new transfer type (`COPY` or `CUT`).
        """

        self.__transfer_type = transfer_type



    @property
    def source_paths(self) -> List[str]:
        """
        @overview A property method to get the list of source file/directory paths.

        :return {List[str]} - The list of source paths.
        """

        return self.__source_paths



    @source_paths.setter
    def source_paths(self, source_paths: List[str]) -> None:
        """
        @overview A property method to set the list of source file/directory paths.

        :param source_paths {List[str]} - The new list of source paths.
        """

        self.__source_paths = source_paths



    def is_copy_operation(self) -> bool:
        """
        @overview A method that checks if an operation is of type `COPY`.

        :return {bool} - If `COPY`, the `True` bool value will be returned, `False` otherwise.
        """

        return self.__transfer_type == TransferType.COPY



    def is_cut_operation(self) -> bool:
        """
        @overview A method that checks if an operation is of type `CUT`.

        :return {bool} - If `CUT`, the `True` bool value will be returned, `False` otherwise.
        """

        return self.__transfer_type == TransferType.CUT
    