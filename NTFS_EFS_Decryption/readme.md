====================================================
Process to manually decrypt an EFS encrypted file. 
====================================================
At a high level you need two things:
1. Encrypted File
2. EFS Private Key of any user who has access to the Encrypted Files

If you are not having access to either of these then forget decrypting an EFS encrypted file. 

I followed the below 5 step process:
Step 1: Extract the $EFS and the $DATA attribute (TheSleuthKit toolset)
Step 2: Extract the Encrypted FEK from the $EFS attribute (010 Editor)
Step 3: Export the EFS private key (Windows certmgr.msc and openssl)
Step 4: Extract the FEK (openssl + 010 Editor)
Step 5: Decrypt the $DATA attribute (openssl + 010 Editor)

The videos detailing these steps are available on YouTube:
https://www.youtube.com/playlist?list=PLmW31MWCFahVkyC58bNG0ipJkovjPk-kC

======================================
TSK commands used:
======================================
fls \\.\\n: 

istat \\.\n: 37 

istat \\.\\n: 37-128-2

======================================
OpenSSL commands used:
======================================
Extracting Private Key from PFX:
openssl pkcs12 -in efs.pfx -out private_key.pem -nodes -nocerts

Decrypting information with a Private Key:
openssl rsautl -decrypt -inkey private_key.pem -in efek_reversed.bin -out fek_decrypted.bin 


AES-CBC mode decryption:
openssl enc -aes-256-cbc -d -in data2.bin -K 41FCAB38B716E9D3A27B5297461C66F48A78C4B8C998156F96ABC059C17BD9EB -iv 241816e97b651658738e9144bead8919 -nopad
