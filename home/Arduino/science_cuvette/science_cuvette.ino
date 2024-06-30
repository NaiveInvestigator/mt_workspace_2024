#include <Servo.h>

Servo motor;

int pinServo = 2;

int angle = 0;

void setup() {
  // put your setup code here, to run once:
  motor.attach(pinServo);
  motor.write(angle);

}
//
//void loop() {
//  // put your main code here, to run repeatedly:
//  angle += 30;
//  
//  if (angle < 180){
//    angle=0;
//  }
//
//  motor.write(angle);
//  delay(2000);
//
//}


void loop() {
  // put your 

  motor.write(0);
  delay(1000);
  motor.write(150);
  delay(7000);
  motor.write(0);
  delay(5000);

}
