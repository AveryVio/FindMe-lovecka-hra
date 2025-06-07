// *****************************************************************************
// *****************************************************************************
// Section: Definitions
// *****************************************************************************
// *****************************************************************************

// APP LED BLE
#define APP_LED_BLE_NULL 0
#define APP_LED_BLE_OFF 1
#define APP_LED_BLE_ON 2

// *****************************************************************************
// *****************************************************************************
// Section: Functions and variables
// *****************************************************************************
// *****************************************************************************

// global variable for "turning the device on and off" (not really)
volatile uint8_t onoff_flag;
void onoff_button_callback(uintptr_t context);
volatile uint8_t test_flag; 
/*void test_button_callback(uintptr_t context);*/
volatile uint8_t test_timer_flag;
void test_timer_callback(TC_TIMER_STATUS status, uintptr_t context);