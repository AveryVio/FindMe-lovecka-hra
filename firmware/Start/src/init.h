// *****************************************************************************
// *****************************************************************************
// Section: Definitions
// *****************************************************************************
// *****************************************************************************

// APP LED BLE
#define APP_LED_BLE_NULL 0
#define APP_LED_BLE_OFF 1
#define APP_LED_BLE_ON 2

// APP TRACING STATES
#define APP_TRACING_NULL 0
#define APP_TRACING_OFF 1
#define APP_TRACING_ON 2

// *****************************************************************************
// *****************************************************************************
// Section: Functions and variables
// *****************************************************************************
// *****************************************************************************

// global variable for "turning the device on and off" (not really)
volatile uint8_t onoff_flag;
void onoff_button_callback(uintptr_t context);
//global variables for adding and removing
volatile uint8_t removing_flag;
void removing_button_callback(uintptr_t context);
volatile uint8_t adding_flag;
void add_button_callback(uintptr_t context);
// global variable for timing
volatile uint8_t test_timer_flag;
void test_timer_callback(TC_TIMER_STATUS status, uintptr_t context);