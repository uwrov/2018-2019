//READ THIS: After the panel is initialized, press the 
//red button and wait for another 3 to 5 second and the panel will
//move to void loop() stage
#include <Servo.h>

Servo esc1, esc2;

void setup() {
  Serial.begin(9600);
  esc1.attach(9);
  esc2.attach(8);

  esc1.writeMicroseconds(1500); // initialize the ESC
  esc2.writeMicroseconds(1500);
  delay(3000); // three second delay to allow time for initialization
}

void loop(){
  esc1.writeMicroseconds(moveForward());
  esc2.writeMicroseconds(1500);
}

int moveForward(){
  return 1700;
}
