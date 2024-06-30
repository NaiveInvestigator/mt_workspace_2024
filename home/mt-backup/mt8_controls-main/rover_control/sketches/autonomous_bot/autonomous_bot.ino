int vel = 110;

// left wheels
#define leftWheels_LPWM 10
#define leftWheels_RPWM 11

// right wheels
#define rightWheels_LPWM 6
#define rightWheels_RPWM 5

/*
 * forward --> rw_RPWM, lw_RPWM = True, rw_LPWM, lw_LPWM = False
 * backward --> rw_LPWM, lw_LPWM = True, rw_RPWM, lw_RPWM = False
 * left --> rw_RPWM, lw_LPWM = True, rw_LPWM, lw_RPWM = False
 * right --> rw_LPWM, lw_RPWM = True, rw_RPWM, lw_LPWM = False
 */

void go(int dir){
  // forward, backward, left, right
  String dir_names[5] = {
    "forward", "backward", "left", "right", "stop"    };
  int dirs[5][4] = {
    {
      vel, 0, vel, 0    }
    ,
    {
      0, vel, 0, vel    }
    ,
    {
      vel, 0, 0, vel    }
    ,
    {
      0, vel, vel, 0    }
    ,
    {
      0, 0, 0, 0    }
  };
  // in each direction array, the formation is --> {lw_LPWM, lw_RPWM, rw_LPWM, rw_RPWM}
  // Serial.println(dir_names[dir]);

  analogWrite(leftWheels_LPWM, dirs[dir][0]);
  analogWrite(leftWheels_RPWM, dirs[dir][1]);
  analogWrite(rightWheels_LPWM, dirs[dir][2]);
  analogWrite(rightWheels_RPWM, dirs[dir][3]);

  delay(10);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(leftWheels_LPWM, OUTPUT);
  pinMode(rightWheels_LPWM, OUTPUT);
  pinMode(leftWheels_RPWM, OUTPUT);
  pinMode(rightWheels_RPWM, OUTPUT);

}


int dirz = 4;

void loop()
{
  if (Serial.available() > 0)
  {
    byte readByte = Serial.read();

    if (readByte == 'w')
    {
      dirz = 0;
    }
    else if (readByte == 's')
    {
      dirz = 1;
    }
    else if (readByte == 'a')
    {
      dirz = 2;
    }
    else if (readByte == 'd')
    {
      dirz = 3;
    }
    else if (readByte == '-')
    {
      dirz = 4;
    }
    go(dirz);
  }
}

