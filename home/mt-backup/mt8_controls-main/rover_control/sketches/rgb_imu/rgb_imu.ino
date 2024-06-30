#include <Wire.h>
#include <JY901.h>

#define RPIN 5
#define GPIN 6
#define BPIN 7

long int green_blink_start_time = -1;

bool RSTATE = true;
bool GSTATE = true;
bool BSTATE = true;

void setup() 
{
  Serial.begin(9600);
  pinMode(RPIN, OUTPUT);
  pinMode(GPIN, OUTPUT);
  pinMode(BPIN, OUTPUT);

  updateLights();
}  

void loop() 
{
  //print received data. Data was received in serialEvent;
 
while (Serial.available()) 
 {
  char letter = Serial.read();
  switch (letter){
  case 'r':
    RSTATE = !RSTATE;
    break;
  case 'g':
    //        green_blink_start_time = millis();
    GSTATE = !GSTATE;
    break;
  case 'b':
    BSTATE = !BSTATE;
    break;
  }

  updateLights();
}
}


void updateLights() {
  //  if (green_blink_start_time > 0 && millis() < green_blink_start_time + 4000) {
  //    if (millis() < green_blink_start_time + 500) {
  //      GSTATE = false;
  //    } else if (millis() < green_blink_start_time + 1000) {
  //      GSTATE = true;
  //    } else if (millis() < green_blink_start_time + 1500) {
  //      GSTATE = false;
  //    } else if (millis() < green_blink_start_time + 2000) {
  //      GSTATE = true;
  //    } else if (millis() < green_blink_start_time + 2500) {
  //      GSTATE = false;
  //    } else if (millis() < green_blink_start_time + 3000) {
  //      GSTATE = true;
  //    } else if (millis() < green_blink_start_time + 3500) {
  //      GSTATE = false;
  //    } else {
  //      GSTATE = true;
  //    }
  //  }
  digitalWrite(RPIN, RSTATE);
  digitalWrite(GPIN, GSTATE);
  digitalWrite(BPIN, BSTATE);
}

