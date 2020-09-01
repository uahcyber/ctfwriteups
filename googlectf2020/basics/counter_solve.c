/*
 * counter_solve.c - prints out the values that 'i' will be in check.sv
 * 
 * build: gcc counter_solve.c -o csolve
 * 
 * made by dayt0n
*/
#include <stdio.h>
#include <stdint.h>

int main(int argc, char* argv[]) {
    uint8_t i = 0;
    // determine order
    for(int j = 0; j < 100; j++) {
        printf("%d ",i);
        i += 5;
        i &= 0x7;
    }
    return 0;
}