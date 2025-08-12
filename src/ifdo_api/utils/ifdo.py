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
        parsed_data = _parse_json_string(input_data)

    elif data_format == DataFormat.file:
        if input_file is None:
            raise ValueErrorException(detail="File input is required for 'file' format")
        parsed_data = await _read_and_parse_file(input_file)

    else:
        raise ValueErrorException(detail="Unsupported data format")

    _handle_validation(parsed_data)
    return parsed_data


async def _read_and_parse_file(file: UploadFile) -> dict:
    """Read and parse a file as JSON or YAML.

    Args:
        file (UploadFile): The file to read and parse.

    Raises:
        ValueErrorException: If the file content is not valid JSON or YAML.

    Returns:
        dict: Parsed content of the file.
    """
    raw_data = await file.read()
    text_data = raw_data.decode("utf-8")

    if file.content_type == "application/json":
        try:
            return json.loads(text_data)
        except json.JSONDecodeError as err:
            raise ValueErrorException(detail="Invalid JSON content in the file") from err

    if file.content_type == "application/yaml":
        try:
            return yaml.safe_load(text_data)
        except yaml.YAMLError as err:
            raise ValueErrorException(detail="Invalid YAML content in the file") from err

    raise ValueErrorException(detail="File must be in JSON or YAML format")


def _parse_json_string(data: str) -> dict:
    """Parse a JSON string and return the result.

    Args:
        data (str): JSON string to parse.

    Raises:
        ValueErrorException: If the JSON string is invalid.

    Returns:
        dict: Parsed JSON data.
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError as err:
        raise ValueErrorException(detail="Invalid JSON body") from err


def _handle_validation(ifdo_data: dict) -> None:
    """Validate IFDO data and print errors if any.

    Args:
        ifdo_data (dict): Parsed IFDO data.

    Raises:
        ValueErrorException: If validation errors are found.
    """
    errors = validate_ifdo(ifdo_data=ifdo_data)
    if not errors:
        return
    msg_error = "Validation errors in the output iFDO metadata file:\n"
    msg_error += "".join(f"{format_ifdo_validation_error(err['path'])}: {err['message']}\n" for err in errors)
    # print(msg_error)


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
