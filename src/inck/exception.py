from typing import Any, Tuple


class ParserError(Exception):
    """Raised for argument parsing related errors."""
    pass


class CodecError(Exception):
    """Base exception class for all codec related errors."""
    pass


class InvalidCodecConfigError(CodecError):
    """Raised when an argument passed to the codec constructor is invalid"""

    def __init__(self, config_error_message: str):
        error_message = (
            f"Codec config argument error: {config_error_message}"
        )
        super().__init__(error_message)


class CodecDataBoundsError(CodecError):
    """Raised when the input data size exceeds the maximum data that can be encoded into the image under the specified config"""

    def __init__(self, img_dim: Tuple[int, int], img_bands: int, data_size: int, max_data_size: int, **enc_args: Any):
        enc_args_str = ", ".join(f"{key} {value}" for key, value in (enc_args or {}).items())
        error_message = (
            f"Unable to encode {data_size} bits of data in an image with "
            f"dimensions {img_dim[0]}x{img_dim[1]}, "
            f"{img_bands} channels"
            f"{', and ' + enc_args_str if enc_args_str else ''}. "
            f"Maximum encodable data size is {max_data_size} bits."
        )
        super().__init__(error_message)
