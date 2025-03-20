#include <stdio.h>

int* main( int argc, char *argv[]) {
/*
    FILE *fptr;
    fptr = fopen("./test.txt", "w");
    fputs(argv[0], fptr);
    fclose(fptr);
*/
    printf("%s\n", argv[1]);


    char latitudeGNSS[10]="\0\0\0\0\0\0\0\0\0";
    char longitudeGNSS[10]="\0\0\0\0\0\0\0\0\0";
    printf("%s , %s\n", latitudeGNSS, longitudeGNSS);

    printf("s\n");

    char *GNSSstring = argv[1];
    char dataValidGNSS = GNSSstring[42];
    printf("%s\n", dataValidGNSS);


    printf("Hello, World!\n");
    return 0;
}