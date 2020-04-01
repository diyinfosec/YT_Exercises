rem Author: Ramprasad R
rem Date: 30-Mar-2020
rem Purpose: This file creates 500 sparse files, 50 MB each
for /l %%x in (1, 1, 500) do (
   echo %%x
   fsutil file createnew %%x.txt 0x3200000
   fsutil sparse setflag %%x.txt
   fsutil sparse setrange %%x.txt 0 0x3200000
)
