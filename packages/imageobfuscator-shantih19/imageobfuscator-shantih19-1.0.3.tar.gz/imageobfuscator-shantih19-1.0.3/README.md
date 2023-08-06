# imageobfuscator.py

Encode and decode data in an image using a password

### Usage
    usage: Image Obfuscator [-h] (-d | -e) -i PATH -s SEED [-p--phrase PHRASE] [-o OUTPUT] [-f] [-x [XOR]]

	Encode and decode data in an image using a seed as a "password"

	options:
	-h, --help            show this help message and exit
	-d, --decode          decode (default)
	-e, --encode          encode
	-i PATH, --path PATH  image path
	-s SEED, --seed SEED  seed/password
	-p--phrase PHRASE     phrase to encode
	-o OUTPUT, --output   OUTPUT output path
	-f, --file            phrase is a path to a file to encode
	-x [XOR], --xor [XOR] xor with another image (blank for original, required for decoding)

### Install

    pip install imageobfuscator-shantih19

### Dependencies
- Python 3.x
- [Pillow](https://github.com/python-pillow/Pillow "Pillow")

### License

This program is distributed AS IS, with no guarantees, under [wtfpl](http://www.wtfpl.net/).

