counter=0

'''
Unicode characters are represented in one of three encoding forms: 
a 32-bit form (UTF32)
a 16-bit form (UTF-16)
an 8-bit form (UTF-8). 

Me:
The 8 in UTF-8 is the minimum bytes per character. For example, a Chinese character encoded with UTF8 will be 3 bytes long. 

The 8-bit, byte-oriented form, UTF-8, has been designed for ease of use with existing ASCII-based systems. 

The Unicode Standard contains 1,114,112 code points, most of which are available for encoding of characters. 
The majority of the common characters used in the major languages of the world are encoded in the 
first 65,536 code points, also known as the Basic Multilingual Plane (BMP). 

The overall capacity for more than 1 million characters is more
than sufficient for all known character encoding requirements, including full coverage of
all minority and historic scripts of the world.
'''
with open('upcase','rb') as f:
	while True:
		f.seek(counter)
		
		file_char=f.read(2)

		if file_char==b'':
			break

		file_char_int = int(counter/2)
		print('file_character',file_char_int)
		#- Surrogate pairs:
		#- High-surrogates: 55296 - 56319
		#- Low-surrogates: 56320 - 57343
		#- From: https://unicodebook.readthedocs.io/unicode_encodings.html
		if file_char_int < 55296 or file_char_int > 57343:
			print('As per chr function ',chr(file_char_int))

		print('As per file ',file_char.decode('utf-16',errors='ignore'))
		print('-----------------------------')
		

		counter=counter+2
		
