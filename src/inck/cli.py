from inck.codec import *
from inck.exception import ParserError, CodecError
from inck.parser import InckParser


def entry():
    parser = InckParser()

    try:
        args = parser.parse_arguments()

        with Image.open(args.image_file) as image:
            if args.codec == 'LSB':
                codec = LSBCodec(args.depth)
            elif args.codec == 'MSB':
                codec = MSBCodec(args.depth)

            if args.mode == 'encode':
                with open(args.input_file, 'rb') as input_file:
                    out_image = codec.encode(image, input_file.read())
                    out_image.save(args.output_file)
            elif args.mode == 'decode':
                out_data = codec.decode(image)
                with open(args.output_file, 'wb') as output_file:
                    output_file.write(out_data)
    except ParserError as e:
        print(e)
        parser.argument_parser.print_help()
    except CodecError as e:
        print(e)
    except Exception as e:
        print(f"An error has occurred during file handling: {e}")
