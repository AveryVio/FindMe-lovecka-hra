/*******************************************************************************
* Copyright (C) 2023 Microchip Technology Inc. and its subsidiaries.
*
* Subject to your compliance with these terms, you may use Microchip software
* and any derivatives exclusively with Microchip products. It is your
* responsibility to comply with third party license terms applicable to your
* use of third party software (including open source software) that may
* accompany Microchip software.
*
* THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
* EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
* WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
* PARTICULAR PURPOSE.
*
* IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
* INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
* WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
* BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
* FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
* ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
* THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
*******************************************************************************/

/*******************************************************************************
  Main Source File

  Company:
    Microchip Technology Inc.

  File Name:
    main.c

  Summary:
    This file contains the "main" function for a project.

  Description:
    This file contains the "main" function for a project.  The
    "main" function calls the "SYS_Initialize" function to initialize the state
    machines of all modules in the system
 *******************************************************************************/

// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************

#include <stddef.h>                     // Defines NULL
#include <stdbool.h>                    // Defines true
#include <stdlib.h>                     // Defines EXIT_FAILURE
#include "definitions.h"                // SYS function prototypes

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
volatile uint8_t onoff_flag = 0;
void onoff_button_callback(uintptr_t context){
onoff_flag = (onoff_flag) ? 0 : 1;
}
// global variable for testting the time
volatile uint8_t test_flag = 0;
/*void test_button_callback(uintptr_t context){
test_flag = 1;
}*/
// global variable for timing
volatile uint8_t test_timer_flag = 0;
void test_timer_callback(TC_TIMER_STATUS status, uintptr_t context){
test_timer_flag = 1;
}

// *****************************************************************************
// *****************************************************************************
// Section: Main Entry Point
// *****************************************************************************
// *****************************************************************************

int main ( void )
{
    /* Initialize all modules */
    SYS_Initialize ( NULL );
    
    uint8_t app_led_ble_state = APP_LED_BLE_NULL;

    
    // register callbacks
    //EIC_CallbackRegister(EIC_PIN_1, test_button_callback, (uintptr_t) NULL);
    EIC_CallbackRegister(EIC_PIN_2, onoff_button_callback, (uintptr_t) NULL);
    TC0_TimerCallbackRegister(test_timer_callback, (uintptr_t) NULL);
    
    // start timer
    TC0_TimerStart();
    TC0_Timer16bitPeriodSet(1024);
    while ( true )
    {
        /* Maintain state machines of all polled MPLAB Harmony modules. */
        SYS_Tasks ( );
        LED_BLE_Set();
        LED_GPS_Set();
 
        // app tasks
        /*if(onoff_flag){
            if(BUTTON_TEST_Get()){test_flag = 1;}
            if(test_flag){
                app_led_ble_state = APP_LED_BLE_ON;
                TC0_Timer16bitCounterSet(1);
            }
            if(test_timer_flag){
                app_led_ble_state = APP_LED_BLE_OFF;
            }
            switch (app_led_ble_state) {
                case APP_LED_BLE_ON:{
                    LED_BLE_Set();
                    break;
                }
                case APP_LED_BLE_OFF:{
                    LED_BLE_Clear();
                    break;
                }
                case APP_LED_BLE_NULL:{
                    app_led_ble_state = APP_LED_BLE_OFF;
                    break;
                }
            }*
            
        }*/
    }

    /* Execution should not come here during normal operation */

    return ( EXIT_FAILURE );
}


/*******************************************************************************
 End of File
*/

