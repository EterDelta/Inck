import argparse

from inck.exception import ParserError


class InckParser:
    """
    Argument parsing class for Inck.
    Responsible for parsing command-line arguments to use the codecs.
    """

    def __init__(self):
        self.argument_parser = argparse.ArgumentParser()
        self.subparsers = self.argument_parser.add_subparsers(dest='mode', help="The mode to run Inck in: encode or decode.")
        self._init_encode_subparser()
        self._init_decode_subparser()

    def _init_encode_subparser(self):
        encode_parser = self.subparsers.add_parser('encode', help="Encode data into an image.")
        encode_parser.add_argument("-c", "--codec", help="Codec type to use.", choices=['LSB', 'MSB'], type=str, required=True)
        encode_parser.add_argument("-d", "--depth", help="Bit depth to use when encoding the data.", type=int, required=True)
        encode_parser.add_argument("-i", "--input_file", help="Path to the input file containing data to be encoded.", type=str, required=True)
        encode_parser.add_argument("-im", "--image_file", help="Path to the image file to encode data into.", type=str,required=True)
        encode_parser.add_argument("-o", "--output_file", help="Path to save the generated image file with encoded data.", type=str, required=True)

    def _init_decode_subparser(self):
        decode_parser = self.subparsers.add_parser('decode', help="Decode data from an image.")
        decode_parser.add_argument("-c", "--codec", help="Codec type to use.", choices=['LSB', 'MSB'], type=str, required=True)
        decode_parser.add_argument("-d", "--depth", help="Bit depth to use when decoding the data.", type=int, required=True)
        decode_parser.add_argument("-im", "--image_file", help="Path to the image file containing encoded data.", type=str, required=True)
        decode_parser.add_argument("-o", "--output_file", help="Path to save the decoded data.", type=str, required=True)

    def parse_arguments(self) -> argparse.Namespace:
        args = self.argument_parser.parse_args()
        if args.mode is None:
            raise ParserError("Please specify an Inck mode.")
        return args
