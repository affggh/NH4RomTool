/* C source file written by affggh */

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>

#include <unistd.h>

#define author "affggh"
#define BUFREADSIZE 4096

using namespace std;

bool ArgFlag = 0;

void Usage(char *self);
int CompareMagic(char *buffer, int bufoff,const char *buf, int size);

int main (int argc, char *argv[]) {
	
	int result;
	char *fileName;
	
	opterr = 0;
	
	while( (result = getopt(argc, argv, "i:h")) != -1 ) // 读参
	{
		switch(result)
		{
			case 'i':
				fileName = optarg;
				// cout << fileName << endl;
				ArgFlag = 1;
				break;
			case 'h':
				Usage(argv[0]);
				return 0;
				break;
			case '?':
				cerr << "Error : invalid argument" << endl;
				Usage(argv[0]);
				return 1;
				break;
			default:
				cerr << "Error : no argument" << endl;
				cerr << " use ih show usage" << endl;
				break;
		}
	}
	if(ArgFlag==0) {
		cerr << "Error : no argument" << endl;
		cerr << " use -h show usage" << endl;
		return 1;
	}

	if(access(fileName, R_OK)!=0) {
		cerr << "File may not exist..." << endl;
	}

	char buffer[BUFREADSIZE];
	FILE *fp;

	fp = fopen(fileName, "rb");
	fread(buffer, BUFREADSIZE, 1, fp);  // 读取 BUFREADSIZE 字节
	fclose(fp);
	
	const char *Type;
	
	// Compare Magic
	if(CompareMagic(buffer, 0, "OPPOENCRYPT!", 12)==0) {
		Type = "ozip";
	} else if(CompareMagic(buffer, 0, "7z", 2)==0) {
		Type = "7z";
	} else if(CompareMagic(buffer, 0, "PK", 2)==0) {
		Type = "zip";
	} else if(CompareMagic(buffer, 1080, "\x53\xef", 2)==0) {
		Type = "ext";
	} else if(CompareMagic(buffer, 0, "\x3a\xff\x26\xed", 4)==0) {
		Type = "sparse";
	} else if(CompareMagic(buffer, 0, "\x67\x44\x6c\x61", 4)==0) {
		Type = "super";
	} else if(CompareMagic(buffer, 1024, "\xe2\xe1\xf5\xe0", 4)==0) {
		Type = "erofs";
	} else if(CompareMagic(buffer, 0, "CrAU", 4)==0) {
		Type = "payload";
	} else if (CompareMagic(buffer, 0, "AVB0", 4)==0) {
		Type = "vbmeta";
	} else if (CompareMagic(buffer, 0, "\xd7\xb7\xab\x1e", 4)==0) {
		Type = "dtbo";
	} else if(CompareMagic(buffer, 0, "MZ", 2)==0) {
		Type = "Windows exe file";
	} else if(CompareMagic(buffer, 0, ".ELF", 4)==0) {
		Type = "Linux executable binary file";
	} else if(CompareMagic(buffer, 0, "ANDROID!", 8)==0) {
		Type = "boot";
	} else {
		Type = "Unknow";
	}
	char* ext;
	ext = strrchr(fileName, '.');
	if(ext!=NULL) {
		if(strcmp(ext, ".dat")==0) {
			cout << "dat" << endl;
		} else if(strcmp(ext, ".br")==0) {
			cout << "br" << endl;
		} else {
			cout << Type << endl;
		}
	} else {
		cout << Type << endl;
	}
	return 0;	
}


void Usage(char *self) {
	cout << self << " -i <file>" << endl;
	cout << "    -i input file" << endl;
	cout << "        This is to detect file type..." << endl;
	cout << "    Written by " << author << endl;
}

int CompareMagic(char *buffer, int bufoff, const char *buf, int size) {
	char buf2[size];
	char *buf3 = new char[strlen(buf)+1];
	strcpy(buf3, buf);
	int i;
	for(i=0;i<size;i++) {
		buf2[i] = buffer[i+bufoff];
	}
	if(memcmp(buf2, buf3, size)==0) {
		return 0;
	} else {
		return 1;
	}
}