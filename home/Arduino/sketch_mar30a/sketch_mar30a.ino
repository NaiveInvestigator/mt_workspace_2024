int rpwm= 9;
int lpwm = 10;

void setup() {
  // put your setup code here, to run once:
  pinMode(rpwm, OUTPUT);
  pinMode(lpwm, OUTPUT);
  

}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(rpwm, 200);
  analogWrite(lpwm, 0);
//  digitalWrite(dir, HIGH);
  delay(2000);
  digitalWrite(lpwm, 200);
  analogWrite(rpwm, 0);
}
