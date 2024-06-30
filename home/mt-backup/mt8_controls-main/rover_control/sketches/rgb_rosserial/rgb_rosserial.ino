#include <ros.h>
#include <std_msgs/String.h>

#define RATE 10

#define R_PIN 2
#define G_PIN 3
#define B_PIN 4

bool r = false;
bool g = false;
bool b = false;

ros::NodeHandle  nh;

std_msgs::String stateMsg;
ros::Publisher rgbState("rgb_state", &stateMsg);

void togglePin(int pin) {
  digitalWrite(pin, HIGH - digitalRead(pin));
}

void rgbCb(const std_msgs::String& msg) {
  switch (msg.data[0]) {
    case 'r':
      togglePin(R_PIN);
      break;
    case 'g':
      togglePin(G_PIN);
      break;
    case 'b':
      togglePin(B_PIN);
      break;
  }
  char state[7];
  sprintf(state, "R%dG%dB%d", digitalRead(R_PIN), digitalRead(G_PIN), digitalRead(B_PIN));
  stateMsg.data = state;
  rgbState.publish(&stateMsg);
  digitalWrite(LED_BUILTIN, HIGH-digitalRead(LED_BUILTIN));
}

ros::Subscriber<std_msgs::String> rgbTopic("rgb_toggle", rgbCb);

void setup() {
  pinMode(R_PIN, OUTPUT);
  pinMode(G_PIN, OUTPUT);
  pinMode(B_PIN, OUTPUT);
  
  nh.initNode();
  nh.advertise(rgbState);
  nh.subscribe(rgbTopic);
}

void loop() {
  nh.spinOnce();
  delay(1000/RATE);
}
