
from pathlib import Path
import json
from typing import Dict, Any

from am_okay.domain.transfer_buffer import TransferBuffer
from am_okay.domain.transfer_operation import TransferOperation, TransferType



class BufferRepository:
    """
    @overview A repository class responsible for persisting the transfer buffer to a JSON file.

    General responsibilities:
      - Serialize and save the transfer buffer state to JSON
      - Load and restore the transfer buffer state from JSON
      - Handle persistence for both slot-based operations and the default operation.
      - Distinguish between `COPY` and `CUT` operations during persistence
    """


    def __init__(self, path: Path):
        """
        @overview A magic method that initializes the buffer repository using the given path.

        :param path {Path} - JSON file path for persistence.
        """

        self.__path = path



    def load(self) -> TransferBuffer:
        """
        @overview A method to load the transfer buffer state from a JSON file.

        :return {TransferBuffer} - The transfer buffer.
        """

        transfer_buffer = TransferBuffer()


        if not self.__path.exists():
            return transfer_buffer
        

        try:
            raw_text = self.__path.read_text(encoding="utf-8")
            raw_data: Any | Dict[str, Any] = json.loads(raw_text) if raw_text.strip() else {}

        except (json.JSONDecodeError, TypeError) as err:
            return transfer_buffer
        
        except Exception as err:
            return transfer_buffer

        if not isinstance(raw_data, dict):
            return transfer_buffer


        # Load the operation stored in default mode
        default_data = raw_data.get("default")

        if default_data:

            if "copy" in default_data:
                transfer_buffer.set_default_operation(
                    TransferOperation(TransferType.COPY, default_data["copy"])
                )

            elif "cut" in default_data:
                transfer_buffer.set_default_operation(
                    TransferOperation(TransferType.CUT, default_data["cut"])
                )


        # Load the operation stored in slot-based mode
        for key, value in raw_data.items():

            if key == "default":
                continue

            index = int(key)

            if "copy" in value:
                transfer_buffer.set_slot_operation_at(
                    index, TransferOperation(TransferType.COPY, value["copy"])
                )

            elif "cut" in value:
                transfer_buffer.set_slot_operation_at(
                    index, TransferOperation(TransferType.CUT, value["cut"])
                )


        return transfer_buffer


 
    def save(self, transfer_buffer: TransferBuffer) -> None:
        """
        @overview A method to persist the transfer buffer state to a JSON file. 
        The directory is created automatically if it does not exist.

        :param transfer_buffer {TransferBuffer} - The transfer buffer to persist.
        """

        self.__path.parent.mkdir(parents=True, exist_ok=True)

        data: Dict[str, Any] = {}


        # Serialize the operation stored in default mode
        default_operation = transfer_buffer.default_operation
        default_data = self.__to_dict(default_operation)

        if default_data:
            data["default"] = default_data


        # Serialize the operation stored in slot-based mode
        if transfer_buffer.slot_operations:
            for index, slot_operation in transfer_buffer.slot_operations.items():

                slot_data = self.__to_dict(slot_operation)

                if slot_data:
                    data[str(index)] = slot_data


        self.__path.write_text(json.dumps(data, indent=2, ensure_ascii=False))



    def __to_dict(self, transfer_operation: TransferOperation | None) -> dict:
        """
        @overview A method to convert a transfer operation into a dictionary suitable for JSON persistence.

        :param transfer_operation {TransferOperation | None} - The operation to convert.
        
        :return {dict} - An empty dictionary if no operation is provided, otherwise a dictionary 
                with a single key: `copy` or `cut`, mapped to the source paths.
        """

        if not transfer_operation:
            return {}


        data: dict = {}

        if transfer_operation.is_copy_operation():
            data["copy"] = transfer_operation.source_paths

        elif transfer_operation.is_cut_operation():
            data["cut"] = transfer_operation.source_paths


        return data
