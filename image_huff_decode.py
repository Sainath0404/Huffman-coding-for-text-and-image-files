from PIL import Image
from utils import *
# Decoding of Header
def decode_header(bitstream):
    Image_height = from_binary_list(bitstream.read_bits(16))
    Image_width = from_binary_list(bitstream.read_bits(16))
    return (Image_height, Image_width)

# Tree Decoding
def tree_decoding(bitstream):
    flag = bitstream.read_bits(1)[0]
    if flag == 1: # Leaf, read and return symbol
        return from_binary_list(bitstream.read_bits(8))
    left = tree_decoding(bitstream)
    right = tree_decoding(bitstream)
    return (left, right)
# decoding of value
def value_decoding(tree, bitstream):
    bit = bitstream.read_bits(1)[0]
    node = tree[bit]
    if type(node) == tuple:
        return value_decoding(node, bitstream)
    return node
# Pixel Decoding
def pixel_decoding(Image_height, Image_width, tree, bitstream):
    pixels = bytearray()
    for i in range(Image_height * Image_width * 3):
        pixels.append(value_decoding(tree, bitstream))
    return Image.frombytes('RGB', (Image_width, Image_height), bytes(pixels))
# Decompressing the image
def decompress_image(in_file_name, out_file_name):
    print('Decompressed image "%s" -> "%s"' % (in_file_name, out_file_name))

    print('Reading of file')
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')
    stream = InputBitStream(in_file_name)
    print('* Header offset: %d' % stream.bytes_read)
    Image_height, Image_width = decode_header(stream)
    stream.flush() # Ensuring if the next chunk is byte-aligned
    print('* Tree offset: %d' % stream.bytes_read)    
    trimmed_tree = tree_decoding(stream)
    stream.flush() # Ensuring if the next chunk is byte-aligned
    print('* Pixel offset: %d' % stream.bytes_read)
    image = pixel_decoding(Image_height, Image_width, trimmed_tree, stream)
    stream.close()
    print('Read %d bytes.' % stream.bytes_read)
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('Image size: (Image_height=%d, Image_width=%d)' % (Image_height, Image_width))
    print('Trimmed tree: %s' % str(trimmed_tree))
    image.save(out_file_name)
