from abc import ABC, abstractmethod

from PIL import Image

from inck.exception import InvalidCodecConfigError, CodecDataBoundsError


class AbstractInckCodec(ABC):
    """Abstract base class for all Inck codecs."""

    @abstractmethod
    def encode(self, img: Image, data: bytes) -> Image:
        """Encodes data into the specified image."""
        pass

    @abstractmethod
    def decode(self, img: Image,) -> bytes:
        """Decodes data from the specified image."""
        pass


class LSBCodec(AbstractInckCodec):
    """
    Implementation of an LSB (Least Significant Bit) codec.
    Encodes and decodes data into/from the least significant bits of the image's pixels based on a provided depth.
    """

    def __init__(self, depth: int):
        super().__init__()
        if depth < 1 or depth > 8:
            raise InvalidCodecConfigError(
                f"Invalid depth value {depth}. Depth must be between 1 and 8 bits."
            )
        self.depth = depth
        self.depth_mask = (1 << depth) - 1

    def encode(self, img: Image, data: bytes) -> Image:
        bin_data = "".join(format(byte, '08b') for byte in data)
        bin_data = format(len(bin_data), '032b') + bin_data

        data_length = len(bin_data)
        data_pointer = 0

        data_length_cap = img.width * img.height * len(img.getbands()) * self.depth

        if data_length > data_length_cap:
            raise CodecDataBoundsError(
                (img.width, img.height),
                len(img.getbands()),
                data_length,
                data_length_cap,
                depth=self.depth
            )

        pixels = list(img.getdata())
        new_pixels = []

        for pixel in pixels:
            new_pixel = list(pixel)
            for channel in range(len(new_pixel)):
                if data_pointer < data_length:
                    data_chunk = self.align_data_chunk(int(bin_data[data_pointer: data_pointer + self.depth], 2))
                    new_pixel[channel] = ((new_pixel[channel] & ~self.depth_mask) | data_chunk)
                    data_pointer += self.depth
            new_pixels.append(tuple(new_pixel))

        img.putdata(new_pixels)
        return img

    def decode(self, img: Image) -> bytes:
        bin_data = ""

        pixels = list(img.getdata())

        for pixel in pixels:
            for value in pixel:
                data_chunk = self.extract_data_chunk(value)
                bin_data += format(data_chunk, f'0{self.depth}b')

        raw_bin_data_length = int(bin_data[:32], 2)
        raw_bin_data = bin_data[32: 32 + raw_bin_data_length]

        byte_data = bytearray()
        for i in range(0, len(raw_bin_data), 8):
            byte = raw_bin_data[i: i + 8]
            byte_data.append(int(byte, 2))

        return bytes(byte_data)

    def align_data_chunk(self, data_bits: int) -> int:
        """Aligns a data chunk for encoding if necessary."""
        return data_bits

    def extract_data_chunk(self, value: int) -> int:
        """Extracts a data chunk from a pixel value."""
        return value & self.depth_mask


class MSBCodec(LSBCodec):
    """
    Implementation of an MSB (Most Significant Bit) codec.
    Encodes and decodes data into/from the most significant bits of the image's pixels based on a provided depth.
    """

    def __init__(self, depth: int):
        super().__init__(depth)
        self.depth_mask = self.depth_mask << (8 - depth)
        self.depth_pad = 8 - depth

    def align_data_chunk(self, data_bits: int) -> int:
        return data_bits << self.depth_pad

    def extract_data_chunk(self, value: int) -> int:
        return (value & self.depth_mask) >> self.depth_pad
