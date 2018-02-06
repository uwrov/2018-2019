#include <Servo.h>
#include <Wire.h>

typedef struct Motor {
  int pin;
  int spd;
  Servo servo;
};

/* *** PACKET HEADERS and CONSTANTS *** */

const int PACKET_SIZE = 4;

/* headers for incoming data */
const int HEADER_KEY_IN_1 = 17;
const int HEADER_KEY_IN_2 = 151;

/* control bytes */

const int HEADER_KEY_LIGHT = 101; // switching LED state
const int HEADER_KEY_PING = 102; // returning ping
const int HEADER_KEY_QUERY_MOTOR_SPEED = 103; // Ask for speed of motor


/* headers for outgoing data */
const int HEADER_KEY_OUT_1 = 74;
const int HEADER_KEY_OUT_2 = 225;


/* *** TIME CONSTANTS *** */

const int DELAY_COUNTER = 5; // delay each loop (ms)
const int SENSOR_ITERATION = 10;  // number of times loop() must be executed in order for sensor data to be read and sent.


/* ** LED ** */

const int LED_PIN = 13;
int ledState = LOW;  // Is the LED on or off?


/* *** SENSOR CONSTANTS and GLOBALS *** */

const int NUM_SENSORS = 6;
const int SENSOR_PORTS[NUM_SENSORS] = {A0, A1, A2, A3, A4, A5};
int sensorLoopCounter = 0;


/* *** MOTOR CONSTANTS and GLOBALS *** */

// Value written to a motor that stops it from spinning; also the init value for the ESC.
const int MOTOR_ZERO = 1500;
// motor range is MOTOR_ZERO +- MOTOR_HALF_RANGE
const int MOTOR_HALF_RANGE = 360;
const int MOTOR_MIN_SPEED = MOTOR_ZERO - MOTOR_HALF_RANGE;
const int MOTOR_MAX_SPEED = MOTOR_ZERO + MOTOR_HALF_RANGE;

// Total number of motors.  Typically used for looping constructs and array inits.
const int NUM_MOTORS = 6;
// Corresponds to a motor's pin number that its ESC is wired to on the Arduino.
const int MOTOR_PINS[NUM_MOTORS] = {2, 3, 4, 5, 6, 7};

// Where motor structs are stored as values
Motor Motors[NUM_MOTORS];



/* *** MOTOR FUCTIONS *** */

// Compute and set new motor speed given an 8-bit byte.
// Scales byte to the motor's speed range and adds to motor's minimum speed.
// Only changes the "spd" field of the motor struct; does not change
// the real-world, physical speed of the spinning motor.
// User must call fire_motor() for speed changes to take physical effect.
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
// Keeps motor speeds within acceptable operating ranges
void set_motor_speed (Motor *motor, int newspeed) {
  if (newspeed < MOTOR_MIN_SPEED) {
    motor->spd = MOTOR_MIN_SPEED;
  } else if (newspeed > MOTOR_MAX_SPEED) {
    motor->spd = MOTOR_MAX_SPEED;
  } else {
    motor->spd = newspeed;
  }
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

/* ** LED ** */

void handle_led() {
  digitalWrite(LED_PIN, ledState);
}

/* *** COMMUNICATION *** */

void write_packet (int byte1, int byte2) {
  Serial.write(HEADER_KEY_OUT_1);
  Serial.write(HEADER_KEY_OUT_2);
  Serial.write(byte1);
  Serial.write(byte2);
}

void send_sensor_data() {
  for (int i = 0; i < NUM_SENSORS; i++) {
    // Send a packet containing the sensor index number and its value
    write_packet(i, analogRead(SENSOR_PORTS[i]));
  }
}

void read_and_discard_n_packets (int n) {
  int i;
  for (i = 0; i < n; i++) {
    Serial.read();
  }
}

void read_and_discard_one_packet () {
  Serial.read();  // :)
}

int read_and_verify_next_packet_headers () {
  return (Serial.read() == HEADER_KEY_IN_1 && Serial.read() == HEADER_KEY_IN_2);
}

void read_and_process_packets () {
  int control_byte, motor_power_byte;
  while (Serial.available() >= PACKET_SIZE) {
    if (read_and_verify_next_packet_headers()) {
      control_byte = Serial.read();
      switch (control_byte) {
      case HEADER_KEY_LIGHT:  // Toggle LED
        ledState = !ledState;
        read_and_discard_one_packet();
        break;
      case HEADER_KEY_PING:   // Ping back to surface
        write_packet(HEADER_KEY_PING, Serial.read());
        break;
      case HEADER_KEY_QUERY_MOTOR_SPEED:
        //        int power = (int)((float)motor_power_byte * (2. * (float)MOTOR_HALF_RANGE / 256.) + (float)MOTOR_MIN_SPEED);
        // send speed of motor indicated by next byte back to surface
        write_packet(HEADER_KEY_QUERY_MOTOR_SPEED,
                     255 * (Motors[Serial.read()].spd - (float)MOTOR_MIN_SPEED) / (float)MOTOR_HALF_RANGE / 2.);
        break;
      default:                // Packet assumed to control motors
        // Control byte is assumed to refer to the motor number (array index)
        motor_power_byte = Serial.read();
        compute_and_set_new_motor_speed(&Motors[control_byte], motor_power_byte);
        break;
      }
    }
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
  read_and_process_packets();
  fire_all_motors();
  handle_led();
  // read and send sensor data every SENSOR_ITERATION iterations
  if (++sensorLoopCounter == SENSOR_ITERATION) {
    sensorLoopCounter = 0;
    send_sensor_data();
  }

  delay(DELAY_COUNTER);
}
