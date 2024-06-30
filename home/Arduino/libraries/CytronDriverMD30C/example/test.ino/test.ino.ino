#include <CytronDriverMD30C.h>

CytronDriverMD30C wheel(3, 5);

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  wheel.setRawSpeed(-100);
  delay(1000);
  wheel.stop_();
  delay(1000);
  wheel.setSpeedLevel(4);
  delay(1000);
  wheel.stop_();
  delay(1000);
  
}
