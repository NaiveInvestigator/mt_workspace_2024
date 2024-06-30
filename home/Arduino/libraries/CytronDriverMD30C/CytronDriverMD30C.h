/*

  CytronDriverMD30C.h - Library for ease use of Cytron MD30C motor driver.
  Created by Al Mahir Ahmed, October 6th 2023.
  Released into the public domain.
  Contact: mahirgored@gmail.com; Github: Vulcan758

*/

#ifndef CytronDriverMD30C_h
#define CytronDriverMD30C_h

#include "Arduino.h"

class CytronDriverMD30C{
    public:
        void setSpeedLevel(int level);
        void setRawSpeed(int val);
        void stop_();
        CytronDriverMD30C(int PWM_, int DIR_); // Short R_EN and L_EN to 5V
    private:
        int PWM;
        int DIR;
};

#endif

