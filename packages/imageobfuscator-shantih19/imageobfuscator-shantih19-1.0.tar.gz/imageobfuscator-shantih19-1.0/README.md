# imageobfuscator.py

Encode and decode data in an image using a password

### Usage
    usage: Image Obfuscator [-h] [-d | -e] [-o [OUTPUT]] [-f] path seed [phrase]
    
    Encode and decode data in an image using a seed as a "password"
    
    positional arguments:
      path                  image path
      seed                  seed/password
      phrase                phrase to encode
    
    options:
      -h, --help            show this help message and exit
      -d, --decode          decode (default)
      -e, --encode          encode
      -o [OUTPUT], --output [OUTPUT]
                            output path
      -f, --file            phrase is a path to a file to encode

### Dependencies
- Python 3.x
- [Pillow](https://github.com/python-pillow/Pillow "Pillow")

### License

This program is distributed AS IS, with no guarantees, under [wtfpl](http://www.wtfpl.net/).

