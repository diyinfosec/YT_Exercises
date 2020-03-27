import struct
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify

# Function to get the Initialization Vector (IV) used by EFS for AES encrypted files. 
def get_iv_for_block(inp_block_num):
#{

	block_offset=efs_block_size*(inp_block_num-1);

	#- NTFS EFS uses a hard-coded IV. 
	#- Ref: https://github.com/nats/ntfsprogs/blob/master/ntfsprogs/ntfsdecrypt.c#L1315
	iv_part1=0x5816657be9161312 + int(block_offset); 
	iv_part2=0x1989adbe44918961 + int(block_offset);

	#- To swap endianness in Python it's easy to use the struct module. 
	#- First you "pack" the IV as a set of little-endian bytes. 
	#- Second, you "unpack" the bytes in the IV as big-endian. So effectively you have converted the endianness!
	le_iv_part1=hex(struct.unpack('>Q',struct.pack("<Q", iv_part1))[0])
	le_iv_part2=hex(struct.unpack('>Q',struct.pack("<Q", iv_part2))[0])


	s=(le_iv_part1 + le_iv_part2).replace('0x','').replace('L','');
	return s;

#}

'''
#- For testing the IV function
for x in range(1,10):
	print get_iv_for_block(x)
'''

#- These two inputs need to be changed depending on the file that you are going to decrypt. 
filename='05-encrypted_cluster.bin'
aes_key_str = "41FCAB38B716E9D3A27B5297461C66F48A78C4B8C998156F96ABC059C17BD9EB";


#- EFS performs encryption in 512 byte blocks at a time. 
#- Ref: https://support.microsoft.com/en-us/help/2739159/files-are-corrupted-after-you-encrypt-them-with-ecc-certificates-by-us
efs_block_size=512

#- Setting the output encoding to utf-8. 
output_encoding='utf-8'

#- When initializing the AES cipher in PyCrypto, we need to give the AES key as a byte stream. 
#- So converting the hex string to byte stream using "unhexlify"
aes_key_bytes=unhexlify(aes_key_str)

#- Variable to keep track of the number of EFS blocks read. 
block_counter=1;

#- String to hold the output of the decryption encoded as per the output_encoding specified. 
decryption_output=''

#- Open the encrypted file for processing. 
#- The file is opened in read-only and binary mode. 

with open(filename, 'rb') as f:
	print('\nFile: %s\n\n-----------------------------------\nPrinting decryption status...\n-----------------------------------'%filename)
	#- This is an infinite while loop that breaks when there are no more bytes to be read from the input file. 
	while True:
		cipher_text = f.read(efs_block_size)

		if not cipher_text:
			break

		'''
		AES Decryption logic. 
		We are using the PyCrypto library to take care of the crypto. 
		You might need to "pip install pycryptodome"
		
		The decryption is pretty straightforward. There are 3 steps:
		1. Get the IV for the EFS block by calling get_iv_for_block
		2. Initialize the algorithm/cipher and pass the encrypted data, AES mode (CBC in this case) and IV
		3. Call the decrypt function of the cipher (initialized in step 2)
		'''
		#- PyCrypto needs the IV to be in bytes, so using unhexlify to convert hex string to bytes. 
		iv=unhexlify(get_iv_for_block(block_counter))

		#- Initializing the AES cipher. 
		cipher = AES.new(aes_key_bytes, AES.MODE_CBC,iv)
		
		#- Decrypting the encrypted text using the AES cipher. 
		plain_text = cipher.decrypt(cipher_text)
		try:
			print("Decryption successful for block %d." %(block_counter))
			decryption_output =	decryption_output + plain_text.decode(output_encoding)
		except ValueError:
			print("Key incorrect or message corrupted")
		
		#- Incrementing block_counter to keep track of number of blocks processed. 
		#- Not using this value for anything but printing in the output. But thought it would be useful to have. 
		block_counter=block_counter+1;

print('\n------------------------------\nResult of the decryption is:\n------------------------------')
print(decryption_output)
