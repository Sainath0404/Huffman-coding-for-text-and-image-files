from huffman import HuffmanCoding
import sys
from pdb import set_trace as bp
from PIL import Image
import numpy as np
import os
from PIL import ImageChops
import argparse
from image_huff_encode import compress_image
from image_huff_decode import decompress_image
import time

parser = argparse.ArgumentParser(description='Huffman Compression & Decompression')
parser.add_argument('--input', type=str, help='Provide Input File Path')
parser.add_argument('--text', action='store_true',help='If text file, invoke this flag')
parser.add_argument('--image', action='store_true',help='If image file, invoke this flag')
parser.add_argument('--compress', action='store_true',help='If Compression, invoke this flag')
parser.add_argument('--decompress', action='store_true',help='If Decompression, invoke this flag')
parser.add_argument('--mapping', type=str,help='If Decompression and text, provide mapping file')

args = parser.parse_args()


if args.image and args.compress:
    filename, file_extension = os.path.splitext(args.input)
    compress_image(args.input, filename+'_compressed.txt')

if args.text and args.compress:
    path = args.input
    h = HuffmanCoding(path)
    output_path = h.compress()
    print("Compressed file path: " + output_path)

if args.text and args.decompress:
    output_path = args.input
    h = HuffmanCoding(output_path)
    decom_path = h.decompress(output_path,args.mapping)
    print("Decompressed file path: " + decom_path)

if args.image and args.decompress:
    filename, file_extension = os.path.splitext(args.input)
    decompress_image(args.input, filename.split('_')[0]+'_decompressed.png')
