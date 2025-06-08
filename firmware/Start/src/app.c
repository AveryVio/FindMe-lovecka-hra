// DOM-IGNORE-BEGIN
/*******************************************************************************
* Copyright (C) 2022 Microchip Technology Inc. and its subsidiaries.
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
// DOM-IGNORE-END

/*******************************************************************************
  MPLAB Harmony Application Source File

  Company:
    Microchip Technology Inc.

  File Name:
    app.c

  Summary:
    This file contains the source code for the MPLAB Harmony application.

  Description:
    This file contains the source code for the MPLAB Harmony application.  It
    implements the logic of the application's state machine and it may call
    API routines of other MPLAB Harmony modules in the system, such as drivers,
    system services, and middleware.  However, it does not call any of the
    system interfaces (such as the "Initialize" and "Tasks" functions) of any of
    the modules in the system or make any assumptions about when those functions
    are called.  That is the responsibility of the configuration-specific system
    files.
 *******************************************************************************/

// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************
#include <string.h>
#include <stdio.h>
#include "app.h"
#include "definitions.h"
#include "app_ble.h"
#include "app_timer.h"
#include "app_led.h"
#include "app_key.h"
#include "app_pxpr.h"

#include "init.h"
// *****************************************************************************
// *****************************************************************************
// Section: Global Data Definitions
// *****************************************************************************
// *****************************************************************************





// *****************************************************************************
/* Application Data

  Summary:
    Holds application data

  Description:
    This structure holds the application's data.

  Remarks:
    This structure should be initialized by the APP_Initialize function.

    Application strings and buffers are be defined outside this structure.
*/

APP_DATA appData;

// *****************************************************************************
// *****************************************************************************
// Section: Application Callback Functions
// *****************************************************************************
// *****************************************************************************

/* TODO:  Add any necessary callback functions.
*/

// *****************************************************************************
// *****************************************************************************
// Section: Application Local Functions
// *****************************************************************************
// *****************************************************************************


/* TODO:  Add any necessary local functions.
*/

unsigned char Ql_Check_XOR(const unsigned char *pData, unsigned int Length) {
    unsigned char result = 0;
    unsigned int i = 0;
    if((NULL == pData) || (Length < 1)){
        return 0;
    }
    for(i = 0; i < Length; i++) {
        result ^= *(pData + i);
    }
    return result;
}

char* USER_GetMSG(){
    char* msg;
    scanf("%s", &msg);
    return msg;
}

int USER_CheckValidity_of_PMTKMSG(char* msg){
    
    if (msg[12] == '0') return 0;//invalid packet
    else if (msg[12] == '1') return 1;//unsupported packet type
    else if (msg[12] == '2') return 2;//valid packet action failed
    else if (msg[12] == '3') return 3;//valid packet action succeeded
}
int USER_CheckValidity_of_PQMSG(char* msg,int chpos){
    if (msg[chpos] == 'O') return 0;//OK
    else if (msg[chops] == 'E') return 1;//ERROR
}

void USER_ChangeBLEResponseData(uint8_t* data, int length){
    BLE_GAP_AdvDataParams_T         appScanRspData;

    //Configure advertising scan response data
    appScanRspData.advLen=length;
    (void)memcpy(appScanRspData.advData, data, appScanRspData.advLen);     /* Scan Response Data */
    BLE_GAP_SetScanRspData(&appScanRspData);
}

int USER_InitializeGPS(){
    printf("$PMTK104*37\r\n");//cold start
    vTaskDelay(300);
    printf("$PMTK220,1000*1F\r\n");
    if (USER_CheckValidity_of_PMTKMSG(USER_GetMSG()) != 3) return 0;//set interval to 1000
    vTaskDelay(300);
    printf("$PMTK353,$PMTK353,1,1,1,0,0*2A\r\n");//start gps, glonass, galileo
    if (USER_CheckValidity_of_PMTKMSG(USER_GetMSG()) != 3) return 0;
    printf("$PQECEF,W,1,1*7F");//enable output
    if (USER_CheckValidity_of_PQMSG(USER_GetMSG()) != 1) return 0;
    return 1;
}

int USER_SuspendGPS(){
    printf("$PMTK161,0*28\r\n");
    if (USER_CheckValidity_of_PMTKMSG(USER_GetMSG()) != 3) return 0;
    return 1;
}

int USER_StartStopGPSLogger(char start_or_stop){ //start = 0, stop = 1
    if(start_or_stop == 0) {
        printf("$PMTK185,0*23");
        if (USER_CheckValidity_of_PMTKMSG(USER_GetMSG()) != 3) return 0;
    }
    else {
        printf("$PMTK185,1*23");
        if (USER_CheckValidity_of_PMTKMSG(USER_GetMSG()) != 3) return 0;
    }
    return 1;
}

void USER_Tasks(void* parameter){
    uint8_t app_led_ble_state = APP_LED_BLE_NULL;
    uint8_t app_tracing_state = APP_TRACING_NULL;

    
    // register callbacks
    EIC_CallbackRegister(EIC_PIN_1, add_button_callback, (uintptr_t) NULL);
    EIC_CallbackRegister(EIC_PIN_2, onoff_button_callback, (uintptr_t) NULL);
    EIC_CallbackRegister(EIC_PIN_0, removing_button_callback, (uintptr_t) NULL);
    TC0_TimerCallbackRegister(test_timer_callback, (uintptr_t) NULL);
    
    // start timer
    TC0_TimerStart();
    TC0_Timer16bitPeriodSet(1024);
    
    while(1){
        // app tasks
        if(onoff_flag){
            //handle button flags
            if(BUTTON_TEST_Get()){
                app_led_ble_state = APP_LED_BLE_ON;
                TC0_Timer16bitCounterSet(1);
                test_flag = 0;
            }
            else if(test_timer_flag){
                app_led_ble_state = APP_LED_BLE_OFF;
                TC0_Timer16bitCounterSet(1);
                test_timer_flag = 0;
            }
            //handle states
            switch (app_led_ble_state) {
                case APP_LED_BLE_ON:{
                    // set led state to on
                    break;
                }
                case APP_LED_BLE_OFF:{
                    // set led state to off
                    break;
                }
                case APP_LED_BLE_NULL:{
                    app_led_ble_state = APP_LED_BLE_OFF;
                    break;
                }
            }
            if((removing_flag) && (adding_flag)){
                app_tracing_state = (app_tracing_state == APP_TRACING_ON) ? APP_TRACING_OFF : APP_TRACING_ON;
                removing_flag = 0;
                adding_flag = 0;
            }
            switch (app_tracing_state) {
                case APP_TRACING_ON:{
                    break;
                }
                case APP_TRACING_OFF:{
                    break;
                }
                case APP_TRACING_NULL:{
                    app_tracing_state = APP_TRACING_OFF;
                    break;
                }
            }
        }
    }
}


// *****************************************************************************
// *****************************************************************************
// Section: Application Initialization and State Machine Functions
// *****************************************************************************
// *****************************************************************************

/*******************************************************************************
  Function:
    void APP_Initialize ( void )

  Remarks:
    See prototype in app.h.
 */

void APP_Initialize ( void )
{
    /* Place the App state machine in its initial state. */
    appData.state = APP_STATE_INIT;


    appData.appQueue = xQueueCreate( 64, sizeof(APP_Msg_T) );
    /* TODO: Initialize your application's state machine and other
     * parameters.
     */
    xTaskCreate(USER_Tasks, "USER_Tasks", 1024, NULL, 1, NULL);
}


/******************************************************************************
  Function:
    void APP_Tasks ( void )

  Remarks:
    See prototype in app.h.
 */
void APP_Tasks ( void )
{
    APP_Msg_T    appMsg[1];
    APP_Msg_T   *p_appMsg;
    p_appMsg=appMsg;

    /* Check the application's current state. */
    switch ( appData.state )
    {
        /* Application's initial state. */
        case APP_STATE_INIT:
        {
            bool appInitialized = true;
            //appData.appQueue = xQueueCreate( 10, sizeof(APP_Msg_T) );

            APP_BleStackInit();

            if (appInitialized)
            {
                bool bPaired;
                uint8_t devId;

                appData.state = APP_STATE_SERVICE_TASKS;
                APP_KEY_Init();
                APP_KEY_MsgRegister(APP_KeyFunction);
                APP_LED_Init();
                APP_InitBleConfig();
                bPaired=APP_GetPairedDeviceId(&devId);
                APP_EnableAdv(bPaired ? APP_ADV_TYPE_WITH_BOND_ADV: APP_ADV_TYPE_ADV);
            }
            break;
        }

        case APP_STATE_SERVICE_TASKS:
        {
            if (OSAL_QUEUE_Receive(&appData.appQueue, &appMsg, OSAL_WAIT_FOREVER) == OSAL_RESULT_TRUE)
            {

                if((APP_MsgId_T)p_appMsg->msgId==APP_MSG_BLE_STACK_EVT)
                {
                    // Pass BLE Stack Event Message to User Application for handling
                    APP_BleStackEvtHandler((STACK_Event_T *)p_appMsg->msgData);
                }
                else if((APP_MsgId_T)p_appMsg->msgId==APP_MSG_BLE_STACK_LOG)
                {
                    // Pass BLE LOG Event Message to User Application for handling
                    APP_BleStackLogHandler((BT_SYS_LogEvent_T *)p_appMsg->msgData);
                }
                else if((APP_MsgId_T)p_appMsg->msgId==APP_MSG_LED_TIMEOUT)
                {
                    APP_LED_Elem_T *p_ledElem;
                    uint8_t     instance;
                    APP_TIMER_TmrElem_T *p_tmrElem = p_appMsg->msgData;
                    instance = p_tmrElem->instance;
                    p_ledElem = p_tmrElem-> p_tmrParam;
                    APP_LED_StateMachine(instance, p_ledElem);
                }
                else if((APP_MsgId_T)p_appMsg->msgId==APP_MSG_KEY_SCAN)
                {
                    APP_KEY_Scan();
                }
                else if((APP_MsgId_T)p_appMsg->msgId==APP_MSG_ALERT_TOGGLE)
                {
                    USER_LED_Toggle();
                }
                else
                {
                }
            }
        }
        break;
        /* The default state should never be executed. */
        default:
        {
            /* TODO: Handle error in application's state machine. */
            break;
        }
    }
}


/*******************************************************************************
 End of File
 */
