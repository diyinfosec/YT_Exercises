import struct
from Crypto.Cipher import AES

#block_offset=raw_input('Enter byte offset (decimal): ')


def get_iv_for_block(block_num):
#{

	block_offset=512*(block_num-1);

	iv_part1=0x5816657be9161312 + int(block_offset); 
	iv_part2=0x1989adbe44918961 + int(block_offset);

	le_iv_part1=hex(struct.unpack('>Q',struct.pack("<Q", iv_part1))[0])
	le_iv_part2=hex(struct.unpack('>Q',struct.pack("<Q", iv_part2))[0])


	s=(le_iv_part1 + le_iv_part2).replace('0x','').replace('L','');
	return s;

#}

'''
for x in range(1,10):
	print get_iv_for_block(x)
'''

filename='encrypted_data.bin'
max_size=512
key = bin(0x41FCAB38B716E9D3A27B5297461C66F48A78C4B8C998156F96ABC059C17BD9EB);
print(type(key));

cipher = AES.new(key, AES.MODE_CBC)


block_counter=1;
with open(filename, 'rb') as f:
    while True:

        buf = f.read(max_size)

        if not buf:
            break
        #- Do processing here
        print(get_iv_for_block(block_counter))
        block_counter=block_counter+1;
        #print(buf);



		
		
		
# pip install pycryptodome


'''
plaintext = cipher.decrypt(ciphertext)
try:
    cipher.verify(tag)
    print("The message is authentic:", plaintext)
except ValueError:
    print("Key incorrect or message corrupted")
'''