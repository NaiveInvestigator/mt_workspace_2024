int f = 8;
int b = 9;
int l = 10;
int r = 11;

void setup() {
  pinMode(f, OUTPUT);
  pinMode(b, OUTPUT);
  pinMode(l, OUTPUT);
  pinMode(r, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  while(Serial.available()>0)
  {
    char c = Serial.read();
    if (c == 'w')
    {
      digitalWrite(f, HIGH);
      digitalWrite(b, LOW);
      digitalWrite(l, LOW);
      digitalWrite(r, HIGH);
    }
    else if (c == 's')
    {
      digitalWrite(f, LOW);
      digitalWrite(b, HIGH);
      digitalWrite(l, HIGH);
      digitalWrite(r, LOW);
    }
    else if (c == 'a')
    {
      digitalWrite(f, LOW);
      digitalWrite(b, HIGH);
      digitalWrite(l, LOW);
      digitalWrite(r, HIGH);
    }
    else if (c == 'd')
    {
      digitalWrite(f, HIGH);
      digitalWrite(b, LOW);
      digitalWrite(l, HIGH);
      digitalWrite(r, LOW);
    }
    else if (c == '-')
    {
      digitalWrite(f, LOW);
      digitalWrite(b, LOW);
      digitalWrite(l, LOW);
      digitalWrite(r, LOW);
    }
  }

}
