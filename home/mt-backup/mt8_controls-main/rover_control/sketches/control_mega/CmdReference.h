#include <Arduino.h>
#include "CytronMotorDriver.h"

typedef struct cmd_arm
{
    CytronMD &motor;
    char cmds[2];
    float multiplier[2];
} CmdArmRef;

typedef struct cmd_wheel
{
    char cmd;
    float multiplier[2];
} CmdWheelRef;
