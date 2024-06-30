/*

  IBT.cpp - Library for ease use of IBT2 BTS7960 motor driver.
  Created by Al Mahir Ahmed, October 6th 2023.
  Released into the public domain.
  Contact: mahirgored@gmail.com; Github: Vulcan758

*/

#include "Arduino.h"
#include "CytronDriverMD30C.h"

CytronDriverMD30C::CytronDriverMD30C(int PWM_, int DIR_){
    PWM = PWM_;
    DIR = DIR_;

    pinMode(PWM, OUTPUT);
    pinMode(DIR, OUTPUT);

}

void CytronDriverMD30C::setSpeedLevel(int level){
    int val = map(constrain(abs(level), 0, 10), 0, 10, 0, 255);
    if (level < 0){
        digitalWrite(DIR, HIGH);
        
    }
    else{
        digitalWrite(DIR, LOW);
    }

    analogWrite(PWM, val);

}

void CytronDriverMD30C::setRawSpeed(int value){
    int val = constrain(abs(value), 0, 255);
    if (value < 0){
        digitalWrite(DIR, HIGH);
        
    }
    else{
        digitalWrite(DIR, LOW);
    }

    analogWrite(PWM, val);

}


void CytronDriverMD30C::stop_(){
    analogWrite(PWM, 0);
}