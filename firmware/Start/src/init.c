#include <stdio.h>
#include <stdlib.h>
#include "definitions.h"

// global variable for "turning the device on and off" (not really)
volatile uint8_t onoff_flag = 0;
void onoff_button_callback(uintptr_t context){
onoff_flag = (onoff_flag) ? 0 : 1;
}
//global variables for adding and removing
volatile uint8_t removing_flag = 0;
void removing_button_callback(uintptr_t context){
removing_flag = 1;
}
volatile uint8_t adding_flag = 0;
void add_button_callback(uintptr_t context){
adding_flag = 1;
}
// global variable for timing
volatile uint8_t test_timer_flag = 0;
void test_timer_callback(TC_TIMER_STATUS status, uintptr_t context){
test_timer_flag = 1;
}