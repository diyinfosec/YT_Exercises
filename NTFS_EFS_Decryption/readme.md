
# Process to manually decrypt an EFS encrypted file. 
 
At a high level you need two things:
1. Encrypted File
2. EFS Private Key of any user who has access to the Encrypted Files

If you are not having access to either of these then forget decrypting an EFS encrypted file. 

## I followed the below 5 step process:
* Step 1: Extract the $EFS and the $DATA attribute (TheSleuthKit toolset)
* Step 2: Extract the Encrypted FEK from the $EFS attribute (010 Editor)
* Step 3: Export the EFS private key (Windows certmgr.msc and openssl)
* Step 4: Extract the FEK (openssl + 010 Editor)
* Step 5: Decrypt the $DATA attribute (openssl + 010 Editor)

### The videos detailing these steps are available on YouTube:

[![NTFS EFS Explained](https://img.youtube.com/vi/B4EJg9tNnpc/maxresdefault.jpg)](https://www.youtube.com/playlist?list=PLmW31MWCFahVkyC58bNG0ipJkovjPk-kC "NTFS EFS Explained")

### The files used in each video are available in this GitHub repository. 
The step number is prefixed with the filename, so that it's easier to identify which video uses which of these files. 

* **enc.txt** - The clear text version of the file that was encrypted. 
* **01-encrypted_data.bin** - The NTFS $DATA attribute of enc.txt containing the contents encrypted with an AES-256 bit File Encryption Key (FEK).
* **01-logged_utility_stream.bin** - The NTFS $EFS attribute of enc.txt containing, among other things, an encrypted version of the FEK (EFEK)
* **02-EFEK_for_TEST_user.bin** - The file containing just the EFEK for the TEST user. 
* **02-EFS_DF_PUBLICKEY_DETAILS.bt** - 010 Editor tempate for parsing the $EFS attribute. 
* **02-EFS_LOGGED_UTILITY_STREAM.bt** - 010 Editor template for parsing the $EFS attribute. 
* **03-efs.pfx** - The PFX archive file containing the EFS private key and certificate. 
* **03-efs_private_key.pem** - EFS private key extracted from the PFX using openssl. 
* **04-fek.txt** - The file encryption key (FEK)
* **05-encrypted_cluster.bin** - The entire encrypted cluster on disk (4096 bytes) instead of just limiting to size of the data. 
 






## TSK commands used:

`fls \\.\\n: `

`istat \\.\n: 37` 

`istat \\.\\n: 37-128-2`


## OpenSSL commands used:

#### Extracting Private Key from PFX:
`openssl pkcs12 -in efs.pfx -out private_key.pem -nodes -nocerts`

#### Decrypting information with a Private Key:
`openssl rsautl -decrypt -inkey private_key.pem -in efek_reversed.bin -out fek_decrypted.bin` 


#### AES-CBC mode decryption:
`openssl enc -aes-256-cbc -d -in data2.bin -K 41FCAB38B716E9D3A27B5297461C66F48A78C4B8C998156F96ABC059C17BD9EB -iv 241816e97b651658738e9144bead8919 -nopad`
