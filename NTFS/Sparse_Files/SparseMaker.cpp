// SparseMaker.cpp - taken from https://www.scriptjunkie.us/2016/08/defying-analysis-with-sparse-malware/
#include "pch.h"
#include <Windows.h>
#include <iostream>

using namespace std;
void main(int argc, char** argv) {
	if (argc < 3) {
		cerr << "Usage: " << argv[0] << " file size" << endl;
		return;
	}
	HANDLE h = CreateFileA(argv[1], GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);
	if (h == INVALID_HANDLE_VALUE) {
		cerr << "Cannot open file" << endl;
		return;
	}
	DWORD outlen;
	DeviceIoControl(h, FSCTL_SET_SPARSE, NULL, 0, NULL, 0, &outlen, NULL);
	LARGE_INTEGER newlen;
	newlen.QuadPart = atoll(argv[2]);
	SetFilePointer(h, newlen.LowPart, &newlen.HighPart, FILE_BEGIN);
	SetEndOfFile(h);
	CloseHandle(h);
}
