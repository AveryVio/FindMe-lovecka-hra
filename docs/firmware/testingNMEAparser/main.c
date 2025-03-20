#include <stdio.h>

int main( int argc, char *argv[]) {
/*
    FILE *fptr;
    fptr = fopen("./test.txt", "w");
    fputs(argv[0], fptr);
    fclose(fptr);
*/
    for (int i = 0; i < argc; i++) {
        printf( "%s\n", argv[i]);
    }

    printf("Hello, World!\n");
    return 0;
}