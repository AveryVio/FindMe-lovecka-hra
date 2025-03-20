#include <stdio.h>

int main( int argc, char *argv[]) {

    FILE *fptr;
    fptr = fopen("./test.txt", "w");
    fputs(argv[0], fptr);
    fclose(fptr);

    for (int i = 0; i < argc; i++) {
        fprintf(fptr, "%s\n", argv[i]);
        printf( "%s\n", argv[i]);
    }

    fclose(fptr);
    printf("Hello, World!\n");
    return 0;
}