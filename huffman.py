import heapq
import os
from pdb import set_trace as bp
import numpy as np
# main class
class HuffmanCoding:
	def __init__(self, path):
		self.path = path
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	class HeapNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		# defining comparators less_than or not
		def __lt__(self, other):
			return self.freq < other.freq
                # defining comparators equal or not
		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other, HeapNode)):
				return False
			return self.freq == other.freq

	# functions for compression:

	def make_freq_dict(self, text):
		freq = {}
		for CH in text:
			if not CH in freq:
				freq[CH] = 0
			freq[CH] += 1
		return freq
        # heap is created using the functions
	def make_heap(self, freq):
		for key in freq:
			node = self.HeapNode(key, freq[key])
			heapq.heappush(self.heap, node)
        # Merging of nodes using function
	def merge_nodes(self):
		while(len(self.heap)>1):
			elementnode1 = heapq.heappop(self.heap)
			elementnode2 = heapq.heappop(self.heap)

			merged = self.HeapNode(None, elementnode1.freq + elementnode2.freq)
			merged.left = elementnode1
			merged.right = elementnode2

			heapq.heappush(self.heap, merged)
        # creates codes helper

	def create_code_helper(self, root, present_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = present_code
			self.reverse_mapping[present_code] = root.char
			return

		self.create_code_helper(root.left, present_code + "0")
		self.create_code_helper(root.right, present_code + "1")

        # creation of codes
	def create_codes(self):
		root = heapq.heappop(self.heap)
		present_code = ""
		self.create_code_helper(root, present_code)
        
        # encoding of get_text
	def GetTextEncoded(self, text):
		text_encoded = ""
		for CH in text:
			text_encoded += self.codes[CH]
		return text_encoded

        # padding of encoded text
	def padding_encoded_text(self, text_encoded):
		extra_padding = 8 - len(text_encoded) % 8
		for i in range(extra_padding):
			text_encoded += "0"

		padded_info = "{0:08b}".format(extra_padding)
		text_encoded = padded_info + text_encoded
		return text_encoded

        # defining get byte array
	def get_byte_array(self, padded_text_encoded):
		if(len(padded_text_encoded) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_text_encoded), 8):
			byte = padded_text_encoded[i:i+8]
			b.append(int(byte, 2))
		return b

        # actual compression function
	def compress(self):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".bin"

		with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
			text = file.read()
			text = text.rstrip()

			freq = self.make_freq_dict(text)
			self.make_heap(freq)
			self.merge_nodes()
			self.create_codes()

			text_encoded = self.GetTextEncoded(text)
			padded_text_encoded = self.padding_encoded_text(text_encoded)

			b = self.get_byte_array(padded_text_encoded)
			output.write(bytes(b))

		print("Compression is done")
		np.save('mapping',self.reverse_mapping)
		return output_path


	""" functions for decompression: """

        # removal of additional text
	def remove_padding(self, padded_text_encoded):
		padded_info = padded_text_encoded[:8]
		extra_padding = int(padded_info, 2)

		padded_text_encoded = padded_text_encoded[8:] 
		text_encoded = padded_text_encoded[:-1*extra_padding]

		return text_encoded
        # Decoding the text
	def decode_text(self, text_encoded):
		present_code = ""
		decoded_text = ""

		for bit in text_encoded:
			present_code += bit
			if(present_code in self.reverse_mapping):
				CH = self.reverse_mapping[present_code]
				decoded_text += CH
				present_code = ""

		return decoded_text

        # function for decompression
	def decompress(self, input_path,mapping_file):
		filename, file_extension = os.path.splitext(input_path)
		output_path = filename + "_decompressed" + ".txt"
		self.reverse_mapping = np.load(mapping_file,allow_pickle=True).item()

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""

			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			text_encoded = self.remove_padding(bit_string)

			decompressed_text = self.decode_text(text_encoded)
			
			output.write(decompressed_text)

		print("Decompression is done")
		return output_path

