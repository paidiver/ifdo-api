import json
from enum import Enum
import requests
import yaml
from fastapi import UploadFile
from jsonschema import Draft202012Validator
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
        if input_file.content_type == "application/json":
            try:
                raw_data = await input_file.read()
                input_data = json.loads(raw_data.decode("utf-8"))
            except json.JSONDecodeError as err:
                raise ValueErrorException(detail="Invalid JSON content in the file") from err
        elif input_file.content_type == "application/yaml":
            try:
                raw_data = await input_file.read()
                input_data = yaml.safe_load(raw_data.decode("utf-8"))
            except yaml.YAMLError as err:
                raise ValueErrorException(detail="Invalid YAML content in the file") from err
        else:
            raise ValueErrorException(detail="File must be in JSON or YAML format")

    msg_error = ""
    errors = validate_ifdo(ifdo_data=input_data)
    if errors:
        msg_error = "Validation errors in the output iFDO metadata file:\n"
        for error in errors:
            msg_error += f"{format_ifdo_validation_error(error['path'])}: {error['message']}\n"
        print(msg_error)  # noqa: T201
        # raise ValueErrorException(detail=msg_error)
    return input_data


def format_ifdo_validation_error(text: list) -> str:
    """Format error message.

    Args:
        text (list): List of error messages.

    Returns:
        str: Formatted error message.
    """
    if len(text) > 3:  # noqa: PLR2004
        return f"...{'.'.join(map(str, text[-3:]))}"
    return ".".join(map(str, text))


def validate_ifdo(ifdo_data: dict) -> list:
    """validate_ifdo method.

    Validates input data against iFDO scheme. Raises an exception if the
    data is invalid.

    Args:
        ifdo_data (Dict): parsed iFDO data

    Returns:
        list: List of validation errors.
    """
    ifdo_version = ifdo_data.get("image-set-header", {}).get("image-set-ifdo-version", "v2.1.0")
    if not ifdo_version:
        msg = "No iFDO version found in metadata."
        raise ValueErrorException(msg)
    schema_file_path = f"https://www.ifdo-schema.org/schemas/{ifdo_version}/ifdo.json"
    response = requests.get(schema_file_path, stream=True, timeout=10)
    response.raise_for_status()
    schema = json.loads(response.content)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(ifdo_data), key=lambda e: e.path)
    return [
        {
            "path": list(error.absolute_path),
            "message": error.message,
        }
        for error in errors
    ]
