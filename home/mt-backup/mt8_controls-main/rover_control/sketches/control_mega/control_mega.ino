#include <ros.h>
#include <ros/time.h>
#include <ros/duration.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Twist.h>
#include <rover_control/ControlStatus.h>

#include "CytronMotorDriver.h"
#include "CmdReference.h"

#define ARM_ACT_1_PWM 12
#define ARM_ACT_2_PWM 13
#define ARM_ACT_3_PWM 10
#define CLAW_SPIN_PWM 11
#define ARM_BASE_PWM 8
#define CLAW_GRIP_PWM 9

#define ARM_ACT_1_DIR 22
#define ARM_ACT_2_DIR 24
#define ARM_ACT_3_DIR 26
#define CLAW_SPIN_DIR 28
#define ARM_BASE_DIR 30
#define CLAW_GRIP_DIR 32

#define WHEEL_LEFT_PWM 46
#define WHEEL_RIGHT_PWM 45

#define WHEEL_LEFT_DIR 48
#define WHEEL_RIGHT_DIR 47

float SKID_MULTIPLIER = 0.5;

int RATE = 250;

int SPEED_INC_MULTIPLIER = 4;

#define DEBUG

void pinModeSetup();
void updateWheel();
void stop();

void postStatus();
void postDebug(const char *);

void keycmdCb(const std_msgs::String &);
void cmdvelCb(const geometry_msgs::Twist &);

ros::NodeHandle nh;

rover_control::ControlStatus controlStatusMsg;
std_msgs::String debugMsg;

ros::Subscriber<std_msgs::String> keycmdTopic("rover_control", &keycmdCb);
ros::Subscriber<geometry_msgs::Twist> cmdvelTopic("cmd_vel", &cmdvelCb);

ros::Publisher controlStatusTopic("control_status", &controlStatusMsg);
ros::Publisher debugTopic("debug", &debugMsg);

int maxSpeedArm = 150;
int maxSpeedWheel = 100;

int leftWheelTarget = 0;
int rightWheelTarget = 0;

char currentWheelCmd = '-';
char currentArmCmd = '-';

String allowedWheelCmds = "wsadqezc";

// Override CytronMD class to add getSpeed()
class Cytron : public CytronMD
{
public:
  Cytron(MODE mode, uint8_t pin1, uint8_t pin2) : CytronMD(mode, pin1, pin2) {}

  void setSpeed(int16_t speed)
  {
    _speed = speed;
    CytronMD::setSpeed(_speed);
  }
  int16_t getSpeed() { return _speed; }

private:
  int16_t _speed;
};

Cytron ACT_1(PWM_DIR, ARM_ACT_1_PWM, ARM_ACT_1_DIR);
Cytron ACT_2(PWM_DIR, ARM_ACT_2_PWM, ARM_ACT_2_DIR);
Cytron ACT_3(PWM_DIR, ARM_ACT_3_PWM, ARM_ACT_3_DIR);
Cytron CLAW_SPIN(PWM_DIR, CLAW_SPIN_PWM, CLAW_SPIN_DIR);
Cytron BASE(PWM_DIR, ARM_BASE_PWM, ARM_BASE_DIR);
Cytron CLAW_GRIP(PWM_DIR, CLAW_GRIP_PWM, CLAW_GRIP_DIR);
Cytron WHEEL_LEFT(PWM_DIR, WHEEL_LEFT_PWM, WHEEL_LEFT_DIR);
Cytron WHEEL_RIGHT(PWM_DIR, WHEEL_RIGHT_PWM, WHEEL_RIGHT_DIR);

const CmdArmRef arm_cmds[6] = {
    {ACT_1,
     {'r', 'f'},
     {1, -1}},
    {ACT_2,
     {'t', 'g'},
     {1, -1}},
    {ACT_3,
     {'y', 'h'},
     {1, -1}},
    {CLAW_SPIN,
     {'v', 'b'},
     {1, -1}},
    {BASE,
     {'n', 'm'},
     {1, -1}},
    {CLAW_GRIP,
     {'o', 'p'},
     {1, -1}}};

CmdWheelRef wheel_cmds[8] = {
    {'w', {1, 1}},
    {'s', {-1, -1}},
    {'a', {-1, 1}},
    {'d', {1, -1}}};

void keycmdCb(const std_msgs::String &msg)
{
  if (msg.data[0] == '-')
  {
    stop();
    return;
  }

  if (msg.data[0] == currentArmCmd || msg.data[0] == currentWheelCmd) // if the same command is sent, ignore it
  {
    return;
  }

  for (int i = 0; i < 6; i++) // iterate through arm commands for a match
  {
    for (int j = 0; j < 2; j++)
    {
      if (msg.data[0] == arm_cmds[i].cmds[j])
      {
        currentArmCmd = arm_cmds[i].cmds[j];
        arm_cmds[i].motor.setSpeed(maxSpeedArm * arm_cmds[i].multiplier[j]);

        postStatus();
        break;
      }
    }
  }

  for (int i = 0; i < 8; i++) // iterate through wheel commands for a match
  {
    if (msg.data[0] == wheel_cmds[i].cmd)
    {
      currentWheelCmd = wheel_cmds[i].cmd;

      leftWheelTarget = maxSpeedWheel * wheel_cmds[i].multiplier[0];
      rightWheelTarget = maxSpeedWheel * wheel_cmds[i].multiplier[1];

      leftWheelTarget = constrain(leftWheelTarget, -255, 255);
      rightWheelTarget = constrain(rightWheelTarget, -255, 255);

      break;
    }
  }

  for (int i = 0; i < 4; i++)
  {
    if (msg.data[0] == '1' + i)
    {
      // maxSpeedArm = 100 + 50 * i;
      maxSpeedWheel = 100 + 50 * i;
      break;
    }
  }
}

void cmdvelCb(const geometry_msgs::Twist &msg)
{
  float linear = constrain(msg.linear.x, -10.0, 10.0);
  float angular = constrain(msg.angular.z, -PI, PI);

  int straight = linear / 10.0 * 255; // 10.0 is the max linear velocity
  int turn = angular / PI * 255;      // PI is the max angular velocity

  leftWheelTarget = straight - turn;
  rightWheelTarget = straight + turn;

  leftWheelTarget = constrain(leftWheelTarget, -255, 255);
  rightWheelTarget = constrain(rightWheelTarget, -255, 255);
}

void postStatus()
{
  controlStatusMsg.act1_speed = ACT_1.getSpeed();
  controlStatusMsg.act2_speed = ACT_2.getSpeed();
  controlStatusMsg.act3_speed = ACT_3.getSpeed();
  controlStatusMsg.claw_spin_speed = CLAW_SPIN.getSpeed();
  controlStatusMsg.base_speed = BASE.getSpeed();
  controlStatusMsg.claw_grip_speed = CLAW_GRIP.getSpeed();

  controlStatusMsg.left_speed = WHEEL_LEFT.getSpeed();
  controlStatusMsg.right_speed = WHEEL_RIGHT.getSpeed();

  // postDebug("status");

  controlStatusTopic.publish(&controlStatusMsg);
}

void postDebug(const char *msg)
{
#ifdef DEBUG
  debugMsg.data = msg;
  debugTopic.publish(&debugMsg);
#endif
}

void setup()
{
  pinModeSetup();

  // nh.getHardware()->setBaud(115200);

  nh.initNode();

  nh.subscribe(keycmdTopic);
  nh.subscribe(cmdvelTopic);
  nh.advertise(controlStatusTopic);
  nh.advertise(debugTopic);

  while (!nh.connected())
  {
    nh.spinOnce();
    delay(100);
  }

  if (!nh.getParam("~skid_multiplier", &SKID_MULTIPLIER, 1, 100))
  {
    SKID_MULTIPLIER = 0.5;
  }
  if (!nh.getParam("~increment_speed", &SPEED_INC_MULTIPLIER, 1, 100))
  {
    SPEED_INC_MULTIPLIER = 4;
  }
  if (!nh.getParam("~rate", &RATE, 1, 100))
  {
    RATE = 250;
  }

  wheel_cmds[4] = {'q', {SKID_MULTIPLIER, 1}};
  wheel_cmds[5] = {'e', {1, SKID_MULTIPLIER}};
  wheel_cmds[6] = {'z', {-SKID_MULTIPLIER, -1}};
  wheel_cmds[7] = {'c', {1, -SKID_MULTIPLIER}};

  postDebug(String(SKID_MULTIPLIER).c_str());
  postDebug(String(SPEED_INC_MULTIPLIER).c_str());
  postDebug(String(RATE).c_str());
}

void loop()
{
  unsigned long start = millis();

  nh.spinOnce();
  updateWheel();

  short passed = millis() - start;
  delay(max(1000 / RATE - passed, 0)); // Only delay if tasks finished before cycle time ran out
}

void pinModeSetup()
{
  pinMode(ARM_ACT_1_PWM, OUTPUT);
  pinMode(ARM_ACT_1_DIR, OUTPUT);
  pinMode(ARM_ACT_2_PWM, OUTPUT);
  pinMode(ARM_ACT_2_DIR, OUTPUT);
  pinMode(ARM_ACT_3_PWM, OUTPUT);
  pinMode(ARM_ACT_3_DIR, OUTPUT);
  pinMode(CLAW_SPIN_PWM, OUTPUT);
  pinMode(CLAW_SPIN_PWM, OUTPUT);
  pinMode(ARM_BASE_PWM, OUTPUT);
  pinMode(ARM_BASE_PWM, OUTPUT);
  pinMode(CLAW_GRIP_PWM, OUTPUT);
  pinMode(CLAW_GRIP_DIR, OUTPUT);
  pinMode(WHEEL_LEFT_PWM, OUTPUT);
  pinMode(WHEEL_LEFT_DIR, OUTPUT);
  pinMode(WHEEL_RIGHT_PWM, OUTPUT);
  pinMode(WHEEL_RIGHT_DIR, OUTPUT);
}

void updateWheel() // Non-blocking way to gradually update speed
{
  const int lspeed = WHEEL_LEFT.getSpeed();
  const int rspeed = WHEEL_RIGHT.getSpeed();

  if (lspeed == leftWheelTarget && rspeed == rightWheelTarget)
  {
    return;
  }

  byte lsign = leftWheelTarget - lspeed < 0 ? 1 : 0;
  byte rsign = rightWheelTarget - rspeed < 0 ? 1 : 0;

  // Find ratio of speed delta and set increment values to reach both target at same time
  float ldelta = abs(leftWheelTarget - lspeed);
  float rdelta = abs(rightWheelTarget - rspeed);
  float ratio = ldelta / rdelta;
  uint8_t linc = 1;
  uint8_t rinc = 1;

  if (ratio > 1)
  {
    linc = ratio;
  }
  else
  {
    rinc = 1 / ratio;
  }

  linc *= SPEED_INC_MULTIPLIER;
  rinc *= SPEED_INC_MULTIPLIER;

  // Increment in the direction of the target speed
  // By taking min of increment and delta, we can ensure that the speed will not go over target

  if (lspeed != leftWheelTarget)
  {
    WHEEL_LEFT.setSpeed(lspeed + min(linc, ldelta) * (lsign ? -1 : 1));
  }

  if (rspeed != rightWheelTarget)
  {
    WHEEL_RIGHT.setSpeed(rspeed + min(rinc, rdelta) * (rsign ? -1 : 1));
  }

  postStatus();
}

void stop()
{
  currentArmCmd = '-';
  currentWheelCmd = '-';

  leftWheelTarget = 0;
  rightWheelTarget = 0;

  ACT_1.setSpeed(0);
  ACT_2.setSpeed(0);
  ACT_3.setSpeed(0);
  CLAW_SPIN.setSpeed(0);
  BASE.setSpeed(0);
  CLAW_GRIP.setSpeed(0);

  postStatus();
}
