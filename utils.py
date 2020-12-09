from collections import Counter
from itertools import chain
# count of symbols
def count_symbols(image):
    pixels = image.getdata()
    values = chain.from_iterable(pixels)
    counts = Counter(values).items()
    return sorted(counts, key=lambda x:x[::-1])
# Building tree function
def build_tree(counts) :
    nodes = [entry[::-1] for entry in counts] 
    while len(nodes) > 1 :
        leastTwo = tuple(nodes[0:2]) 
        theRest = nodes[2:] 
        combFreq = leastTwo[0][0] + leastTwo[1][0]  
        nodes = theRest + [(combFreq, leastTwo)] 
        nodes.sort() 
    return nodes[0] # Returns single tree from the inside list
# timming of tree
def trim_tree(tree) :
    p = tree[1] 
    if type(p) is tuple: 
        return (trim_tree(p[0]), trim_tree(p[1]))
    return p # returning of p
# Implementation of assigned codes
def assign_codes_impl(codes, node, pat):
    if type(node) == tuple:
        assign_codes_impl(codes, node[0], pat + [0]) 
        assign_codes_impl(codes, node[1], pat + [1])
    else:
        codes[node] = pat 
# codes assigning
def assign_codes(tree):
    codes = {}
    assign_codes_impl(codes, tree, [])
    return codes

def to_binary_list(n):
    """Converting integer into a list of bits"""
    return [n] if (n <= 1) else to_binary_list(n >> 1) + [n & 1]

def from_binary_list(bits):
    """Conversion of the list of bits into an integer"""
    result = 0
    for bit in bits:
        result = (result << 1) | bit
    return result
# padding of bits
def pad_bits(bits, n):
    """Prefix list of bits with enough zeros to reach n digits"""
    assert(n >= len(bits))
    return ([0] * (n - len(bits)) + bits)
# Defining in-built functions
# Output functions 
class OutputBitStream(object): 
    def __init__(self, file_name): 
        self.file_name = file_name
        self.file = open(self.file_name, 'wb') 
        self.bytes_written = 0
        self.buffer = []

    def write_bit(self, value): 
        self.write_bits([value])

    def write_bits(self, values):
        self.buffer += values
        while len(self.buffer) >= 8:
            self._save_byte()        

    def flush(self):
        if len(self.buffer) > 0: 
            self.buffer += [0] * (8 - len(self.buffer))
            self._save_byte()
        assert(len(self.buffer) == 0)

    def _save_byte(self):
        bits = self.buffer[:8]
        self.buffer[:] = self.buffer[8:]

        byte_value = from_binary_list(bits)
        self.file.write(bytes([byte_value]))
        self.bytes_written += 1

    def close(self): 
        self.flush()
        self.file.close()
# Taking Input functions
class InputBitStream(object): 
    def __init__(self, file_name): 
        self.file_name = file_name
        self.file = open(self.file_name, 'rb') 
        self.bytes_read = 0
        self.buffer = []

    def read_bit(self):
        return self.read_bits(1)[0]

    def read_bits(self, count):
        while len(self.buffer) < count:
            self._load_byte()
        result = self.buffer[:count]
        self.buffer[:] = self.buffer[count:]
        return result

    def flush(self):
        assert(not any(self.buffer))
        self.buffer[:] = []

    def _load_byte(self):
        value = ord(self.file.read(1))
        self.buffer += pad_bits(to_binary_list(value), 8)
        self.bytes_read += 1

    def close(self): 
        self.file.close()
