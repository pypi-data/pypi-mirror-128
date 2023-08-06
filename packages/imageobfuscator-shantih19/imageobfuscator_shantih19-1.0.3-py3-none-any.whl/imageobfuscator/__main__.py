from PIL import Image
import random
import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(prog="Image Obfuscator",description="Encode and decode data in an image using a seed as a \"password\"")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--decode", help='decode (default)', dest='mode', action="store_false")
    group.add_argument('-e', "--encode", help="encode", dest='mode', action="store_true")
    parser.add_argument('-i','--path', help="image path", required=True)
    parser.add_argument('-s','--seed', help="seed/password", required=True)
    parser.add_argument('-p' '--phrase', help="phrase to encode", dest="phrase")
    parser.add_argument('-o', '--output', help="output path", dest='output')
    parser.add_argument('-f', '--file', help="phrase is a path to a file to encode", dest='file', action="store_true")
    parser.add_argument('-x', '--xor', help="xor with another image (blank for original, required for decoding)", dest='xor', nargs='?', const="?")
    args = parser.parse_args()
    filename = args.path
    mode = args.mode
    password = args.seed
    if mode:
        if args.phrase ==  None:
            parser.error("missing phrase to encode")
        if args.file:
            with open( args.phrase ,"rb") as f:
                phrase = f.read()
        else:
            phrase = args.phrase.encode('utf-8')
    
    random.seed(password)
    with Image.open(filename) as img:
        w, h = img.size
        pool = [(x,y) for x in random.sample(range(w), w) for y in random.sample(range(h), h)]
        pool = random.sample(pool, len(pool))
        if mode:
            if img.mode != "RGB":
                img = img.convert("RGB")
            if args.xor == "?":
                key = img
            elif args.xor != None:
                key = Image.open(args.xor)
            length = len(phrase)
            img.putpixel(pool[0], tuple(length.to_bytes(3, 'big')))
            for i in range(0, length, 3):
                v = []
                pixel = pool[i//3+1]
                for b in range(3):
                    if i + b < length:
                        if args.xor != None:
                            v.append( key.getpixel(pixel)[b] ^ phrase[i+b] )
                        else:
                            v.append(  phrase[i+b] )
                    else:
                        v.append(img.getpixel(pixel)[b])
                img.putpixel(pixel, tuple(v))
            if args.output == None:
                img.save(os.path.splitext(filename)[0] + "_encoded.png")
            else:
                img.save(args.output)
            print("Saved.")
        else:
            text = []             
            length = int.from_bytes(img.getpixel(pool[0]),'big')
            print(length)
            if args.xor != None:
                if args.xor != "?":
                    key = Image.open(args.xor)
                    if key.mode != "RGB":
                        key = key.convert("RGB")
                else:
                    parser.error("xor image path is required")
            for i in range(0, length, 3):
                for b in range(3):
                    if b + i < length:
                        if args.xor != None:
                            p = key.getpixel(pool[i//3+1])[b]
                            text.append(p ^ img.getpixel(pool[i//3+1])[b])
                        else:
                            text.append(img.getpixel(pool[i//3+1])[b])
            if args.file:
                if args.output == None:
                    parser.error("--output needed with --file")
                else:
                    with open(args.output, "wb") as f:
                        f.write(bytes(text))
                    print("File saved.")
            else:
                print(bytes(text).decode('utf-8'))

if __name__ == "__main__":
    main()
            