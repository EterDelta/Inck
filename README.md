# Inck


![Language](https://img.shields.io/badge/language-Python%203.6-3572A5.svg?style=flat-square)
![GitHub license](https://img.shields.io/github/license/EterDelta/Inck?style=flat-square)

Inck is a simple Python CLI tool to encode and decode data from images using LSB and MSB steganography.
The project is very simple and doesn't aim to be something serious. But it's a fun experiment to show basics of steganography and people can take advantage of it.

## Installation
To install Inck, simply use pip:
```bash
pip install inck
```
Ensure you have Python 3.6 or higher.

## Usage
Inck offers two codec types to hide data: LSB (Least Significant Bit) and MSB (Most Significant Bit).
The depth parameter adjusts their intensity. Higher depth values increase data capacity at the cost of image distortion.

- **LSB**: As the name suggests, LSB deals with the least significant bits of the pixel values. Any modification is typically harder to perceive by the naked eye. This makes it an ideal choice when visual discretion is essential.
- **MSB**: Manipulating the most significant bits will cause prominent changes to the image's appearance, but enhances the robustness of the encoded data against alterations. For image modifications or compression, MSB might be your best choice.

Keep in mind that Inck doesn't embed any header to identify an image as "encoded"; it only includes essential data information.
As a result, attempting to decode images without encoded data or using incorrect parameters is possible, and will yield corrupted outputs.

### Command Line
Encode:
```bash
inck encode -c codec_type -d depth -i input_data -im input_image -o output_image
```

Decode:
```bash
inck decode -c codec_type -d depth -im input_image -o output_data
```

### As a Library
If for some reason you want to integrate this, Inck codecs can also be used within Python projects:
```python
from inck.codec import LSBCodec, MSBCodec
from PIL import Image

input_image = Image.open('input.png')
input_data = bytes("Your super secret message", 'utf-8') # Or raw file
depth = 1

codec = LSBCodec(depth)

# Encode
output_image = codec.encode(input_image, input_data)
output_image.show()

# Decode
output_data = codec.decode(output_image)
print(output_data)
```

## Usage Example
The examples folder contains an encoded 16x16 32-bit PNG image.
To get started, decode it into an executable using LSB and a depth value of 2.
```bash
inck decode LSB -d 2 -im Pong.png -o Output.exe
```
It looks like a regular Minecraft texture, but when decoding, it's actually a tiny Pong game for Windows x86 and x64!