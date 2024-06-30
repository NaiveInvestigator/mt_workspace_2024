#include <ros.h>
#include<std_msgs/String.h>
#define blue_led 2
#define red_led 3
#define green_led 4


ros::NodeHandle nh;

void exec(const std_msgs::String& rgb_msg){

  if (Serial.available() >0) {
    char receivedChar = Serial.read();
    switch (receivedChar) {
      case 'a':nm  
        digitalWrite(red_led, !(digitalRead(red_led)));
        break;
      case 'b':
        digitalWrite(blue_led, !(digitalRead(blue_led)));
        break;
      case 'c': 
        digitalWrite(green_led, !(digitalRead(green_led)));
        break;
      default:
        break;

    }
  }
}

ros::Subscriber<std_msgs::String> rgb('rgb_msg', &exec);
void setup() {

  pinMode(red_led, OUTPUT);
  pinMode(blue_led, OUTPUT);
  pinMode(green_led, OUTPUT);
  digitalWrite(red_led, HIGH);
  digitalWrite(blue_led, HIGH);
  digitalWrite(green_led, HIGH);
  nh.initNode();
  nh.subscribe(rgb);
  
}


void loop() {
  nh.spinOnce();
  delay(10);
  
}
        
  
  
 
