import json
from enum import Enum
from fastapi import UploadFile
from paidiverpy.metadata_parser.ifdo_tools import format_ifdo_validation_error
from paidiverpy.metadata_parser.ifdo_tools import validate_ifdo
from ifdo_api.api.exceptions import ValueErrorException


class DataFormat(str, Enum):
    """Enum representing the data format for import operations."""

    ifdo = "ifdo"
    file = "file"


async def validate_ifdo_data(data_format: DataFormat, input_data: str | None, input_file: UploadFile | None) -> dict:
    """Validate and parse IFDO data from the provided input."""
    if data_format == DataFormat.ifdo:
        if input_data is None:
            raise ValueErrorException(detail="Invalid IFDO data format")
        try:
            input_data = json.loads(input_data)
        except json.JSONDecodeError as err:
            raise ValueErrorException(detail="Invalid JSON body") from err
    elif data_format == DataFormat.file:
        if input_file is None:
            raise ValueErrorException(detail="File input is required for 'file' format")
        if input_file.content_type != "application/json":
            raise ValueErrorException(detail="File must be in JSON format")
        try:
            raw_data = await input_file.read()
            input_data = json.loads(raw_data.decode("utf-8"))
        except json.JSONDecodeError as err:
            raise ValueErrorException(detail="Invalid JSON content in the file") from err

    msg_error = ""
    errors = validate_ifdo(ifdo_data=input_data)
    if errors:
        msg_error = "Validation errors in the output iFDO metadata file:\n"
        for error in errors:
            msg_error += f"{format_ifdo_validation_error(error['path'])}: {error['message']}\n"
        print(msg_error)  # noqa: T201
        # raise ValueErrorException(detail=msg_error)

    return input_data
