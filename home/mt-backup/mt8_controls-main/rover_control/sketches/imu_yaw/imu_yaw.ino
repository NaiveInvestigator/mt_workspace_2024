#include <Wire.h>
#include <JY901.h>

void setup() 
{
  Serial.begin(9600);
}

void loop() 
{
  //print received data. Data was received in serialEvent;
    Serial.println((float)JY901.stcAngle.Angle[2]/32768*180);
  delay(100);
}

void serialEvent() 
{
  while (Serial.available()) 
  {
    JY901.CopeSerialData(Serial.read()); //Call JY901 data cope function
  }
}
