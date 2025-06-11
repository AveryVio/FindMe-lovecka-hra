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
// Section: Dev Comments
// *****************************************************************************
// *****************************************************************************

// callbacs and functions for app in app.c

// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************

#include <stddef.h>                     // Defines NULL
#include <stdbool.h>                    // Defines true
#include <stdlib.h>                     // Defines EXIT_FAILURE
#include "definitions.h"
#include "ble_gap.h"                // SYS function prototypes


// *****************************************************************************
// *****************************************************************************
// Section: DEfinitions
// *****************************************************************************
// *****************************************************************************

#define BLE_ADVERTIZING_DATA_STRING "0000000000000000000" //maximum 31 characters
#define BLE_ADVERTIZING_DATA_LENGTH sizeof(BLE_ADVERTIZING_DATA_STRING);

// *****************************************************************************
// *****************************************************************************
// Section: Main Entry Point
// *****************************************************************************
// *****************************************************************************

int main ( void )
{
    /* Initialize all modules */
    SYS_Initialize ( NULL );

    BLE_GAP_AdvDataParams_T advertising_dat_struct;
    
    advertising_dat_struct.advLen = BLE_ADVERTIZING_DATA_LENGTH
    (void)memcpy(advertising_dat_struct.advData, BLE_ADVERTIZING_DATA_STRING, advertising_dat_struct.advLen);     /* Advertising Data */
    BLE_GAP_SetAdvData(&advertising_dat_struct);
    
    BLE_GAP_AdvParams_T advertising_params = {8, 32, BLE_GAP_ADV_TYPE_ADV_IND, BLE_GAP_ADV_CHANNEL_ALL, BLE_GAP_ADV_FILTER_DEFAULT};
    
    
    while ( true )
    {
        /* Maintain state machines of all polled MPLAB Harmony modules. */
        SYS_Tasks ( );
    }

    /* Execution should not come here during normal operation */

    return ( EXIT_FAILURE );
}


/*******************************************************************************
 End of File
*/

