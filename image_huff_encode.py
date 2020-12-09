from PIL import Image
from utils import *
# encoding function for compressed data
def compressed_size(counts, codes):
    header_size = 2 * 16 # values of height and width as 16 bit 

    tree_size = len(counts) * (1 + 8) 
    tree_size += len(counts) - 1 
    if tree_size % 8 > 0: 
        tree_size += 8 - (tree_size % 8)

    # count pf symbols
    pixels_size = sum([count * len(codes[symbol]) for symbol, count in counts])
    if pixels_size % 8 > 0: # Padding to next full byte
        pixels_size += 8 - (pixels_size % 8)

    return (header_size + tree_size + pixels_size) / 8
# encoding header
def encode_header(image, bitstream):
    bits_In_height = pad_bits(to_binary_list(image.height), 16)
    bitstream.write_bits(bits_In_height)    
    bits_In_width = pad_bits(to_binary_list(image.width), 16)
    bitstream.write_bits(bits_In_width)
# tree encoding
def tree_encoding(tree, bitstream):
    if type(tree) == tuple: 
        bitstream.write_bit(0)
        tree_encoding(tree[0], bitstream)
        tree_encoding(tree[1], bitstream)
    else: 
        bitstream.write_bit(1)
        symbol_bits = pad_bits(to_binary_list(tree), 8)
        bitstream.write_bits(symbol_bits)
# pixel encoding
def encode_pixels(image, codes, bitstream):
    for pixel in image.getdata():
        for value in pixel:
            bitstream.write_bits(codes[value])
# deifining raw size
def raw_size(width, height):
    header_size = 2 * 16 # values of height and width as 16 bit 
    pixels_size = 3 * 8 * width * height #one channel contains 3 channels, 8 bits
    return (header_size + pixels_size) / 8
# image compression is done
def compress_image(in_file_name, out_file_name):
    print('Compressing "%s" -> "%s"' % (in_file_name, out_file_name))
    image = Image.open(in_file_name).convert('RGB')
    print('Image dimensions: (height=%d, width=%d)' % (image.height, image.width))
    size_raw = raw_size(image.height, image.width)
    print('RAW image size: %d bytes' % size_raw)
    counts = count_symbols(image)
    print('Counts: %s' % counts)
    tree = build_tree(counts)
    print('Tree: %s' % str(tree))
    trimmed_tree = trim_tree(tree)
    print('Trimmed tree: %s' % str(trimmed_tree))
    codes = assign_codes(trimmed_tree)
    print('Codes: %s' % codes)
    print('--------------------------------------------------------------------------------------------------------------------')
    size_estimate = compressed_size(counts, codes)
    print('Estimated size: %d bytes' % size_estimate)
    stream = OutputBitStream(out_file_name)
    print('* Header offset: %d' % stream.bytes_written)
    encode_header(image, stream)
    stream.flush() # Ensuring if the next chunk is byte-aligned
    print('* Tree offset: %d' % stream.bytes_written)
    tree_encoding(trimmed_tree, stream)
    stream.flush() # Ensuring if the next chunk is byte-aligned
    print('* Pixel offset: %d' % stream.bytes_written)
    encode_pixels(image, codes, stream)
    stream.close()

    size_real = stream.bytes_written
    print('Wrote %d bytes.' % size_real)
    print('--------------------------------------------------------------------------------------------------------------------')
    print('Estimation is %scorrect.' % ('' if size_estimate == size_real else 'in'))
    print('Compression ratio: %0.2f' % (float(size_raw) / size_real))
