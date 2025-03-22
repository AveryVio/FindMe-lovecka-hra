#include <stdio.h>

char *strncpy(char *dst, const char *src, size_t n){
   int i;
   char *temp;
   temp = dst;  
   for (i = 0; i < n; i++)
      *dst++ = *src++;
   return temp;
}

struct GNSSDataStruct {
    char latitudeGNSS[10];
    char longitudeGNSS[10];
    char dataValidGNSS;
};

struct GNSSDataStruct extractGNSSdata(char GNSSDataString[57]){
    struct GNSSDataStruct returnGNSSDataStruct = {"","",'V'};
    char latitudeGNSS[10]="\0\0\0\0\0\0\0\0\0";
    char longitudeGNSS[10]="\0\0\0\0\0\0\0\0\0";

    strncpy(returnGNSSDataStruct.latitudeGNSS, GNSSDataString + 7, 9);
    strncpy(returnGNSSDataStruct.longitudeGNSS, GNSSDataString + 19, 9);


    returnGNSSDataStruct.dataValidGNSS =  GNSSDataString[42];

    return returnGNSSDataStruct;
}


int* main( int argc, char *argv[]) {
    printf("%s\n", argv[1]);

    char testing[] = "$GNGLL,3150.7856,N,1171.9479,E,102243.000,A,D*4B<CR><LF>";
    struct GNSSDataStruct outing = extractGNSSdata(testing);
    printf("%s\n", outing.latitudeGNSS);
    printf("%s\n", outing.longitudeGNSS);
    printf("%c\n", outing.dataValidGNSS);
    
    printf("Hello, World!\n");
    return 0;
}