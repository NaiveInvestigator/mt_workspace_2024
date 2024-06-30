#include <ros.h>
#include <std_msgs/String.h>

ros::NodeHandle  nh;
int vel = 150;

void go(int dir){
  // forward, backward, left, right
  String dir_names[5] = {"forward", "backward", "left", "right", "stop"};
  int dirs[5][4] = {{vel, 0, vel, 0}, {0, vel, 0, vel}, {vel, 0, 0, vel}, {0, vel, vel, 0}, {0, 0, 0, 0}};
  // in each direction array, the formation is --> {lw_LPWM, lw_RPWM, rw_LPWM, rw_RPWM}
  // Serial.println(dir_names[dir]);
/*
  analogWrite(leftWheels_LPWM, dirs[dir][0]);
  analogWrite(leftWheels_RPWM, dirs[dir][1]);
  analogWrite(rightWheels_LPWM, dirs[dir][2]);
  analogWrite(rightWheels_RPWM, dirs[dir][3]);
  */
  nh.loginfo(dir_names[dir].c_str());
}

void moveCallback( const std_msgs::String& keys){
  char state = keys.data[0];
  if (isDigit(state)){
    int vel_level = state - '0';
    vel = map(vel_level, 0, 10, 0, 255); 
    nh.loginfo("changing speed to level " + state)
    nh.loginfo("current speed is " 
  }
  else {
      switch (state){
      case 'w':
          digitalWrite(13, HIGH);
          go(0);
          delay(100);
          digitalWrite(13, LOW);
          go(4);
          break;
      case 'a':
          digitalWrite(13, HIGH);
          go(2);
          delay(100);
          digitalWrite(13, LOW);
          go(4);
          break;
      case 's':
          digitalWrite(13, HIGH);
          go(1);
          delay(100);
          digitalWrite(13, LOW);
          go(4);
          break;
      case 'd':
          digitalWrite(13, HIGH);
          go(3);
          delay(100);
          digitalWrite(13, LOW);
          go(4);
          break;
      default:
          digitalWrite(13, LOW);
          go(4);
          break;
    }
  }
}

ros::Subscriber<std_msgs::String> rover("rover_control", &moveCallback );

void setup()
{ 
  pinMode(LED_BUILTIN, OUTPUT);
  nh.initNode();
  nh.subscribe(rover);
}

void loop()
{  
  nh.spinOnce();
  delay(1);
}
