#include <Servo.h>
#include <Wire.h>

typedef struct Motor {
  int pin;
  int spd;
  Servo servo;
};

const int LED_PIN = 13;

// Value written to a motor that stops it from spinning.
// Also the init value for the ESC.
const int MOTOR_ZERO = 1500;
const int MOTOR_HALF_RANGE = 360;  // motor range is MOTOR_ZERO +- MOTOR_HALF_RANGE
const int MOTOR_MIN_SPEED = MOTOR_ZERO - MOTOR_HALF_RANGE;
const int MOTOR_MAX_SPEED = MOTOR_ZERO + MOTOR_HALF_RANGE;

// Total number of motors.  Typically used for looping constructs and array inits.
const int NUM_MOTORS = 6;
// Corresponds to a motor's pin number that its ESC is wired to on the Arduino.
const int MOTOR_PINS[NUM_MOTORS] = {2, 3, 4, 5, 6, 7};

Motor Motors[NUM_MOTORS];

void compute_and_set_new_motor_speed (Motor *motor, int motor_power_byte) {
  int power = (int)((float)motor_power_byte * (2. * (float)MOTOR_HALF_RANGE / 256.) + (float)MOTOR_MIN_SPEED);
  motor->spd = power;
}

// Attaches an Arduino pin to a motor and sets the pin field in the struct.
// Must be called before any value is written to it so that
// communication is set up with the ESC
void attach_motor_to_pin (Motor *motor, int pin) {
  motor->pin = pin;
  motor->servo.attach(pin);
}

// Abstraction: sets a motor's speed field to the supplied value.
// Keeps motor speeds within the acceptable operating ranges
void set_motor_speed (Motor *motor, int newspeed) {
  motor->spd = newspeed;  // Add in error checking code later
}

// Takes a motor struct's speed and writes it to the ESC.
// Calling this actually spins the motor.
void fire_motor (Motor *motor) {
  motor->servo.writeMicroseconds(motor->spd);
}

// Sets the motor's speed to its zero value, stopping it from spinning.
// Effective immediately (fire_motor() is called)
void zero_motor (Motor *motor) {
  set_motor_speed(motor, MOTOR_ZERO);
  fire_motor(motor);
}

void init_all_motors () {
  int i;
  for (i = 0; i < NUM_MOTORS; i++) {
    attach_motor_to_pin(&Motors[i], MOTOR_PINS[i]);
    zero_motor(&Motors[i]);
  }
}

void fire_all_motors () {
  int i;
  for (i = 0; i < NUM_MOTORS; i++) {
    fire_motor(&Motors[i]);
  }
}

void setup() {
  // Initialize comms.
  Serial.begin(9600);
  Wire.begin();

  init_all_motors();

  delay(3000); // Part of motor initialization routine
  pinMode(LED_PIN, OUTPUT);
  
}

void loop() {
  while (Serial.available() >= 2) {
    int motor_number = Serial.read();
    int motor_power_byte = Serial.read();
    compute_and_set_new_motor_speed(&Motors[motor_number], motor_power_byte);
  }
  fire_all_motors();
}
