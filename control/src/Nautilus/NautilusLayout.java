package Nautilus;

import ROVControl.ROVLayout;
import ROVControl.ROVState;
import com.pi4j.component.servo.ServoDriver;
import com.pi4j.component.servo.ServoProvider;
import com.pi4j.component.servo.impl.RPIServoBlasterProvider;
import com.pi4j.io.gpio.GpioPin;
import com.pi4j.io.gpio.Pin;
import com.pi4j.io.gpio.RaspiPin;

import java.io.File;
import java.io.IOException;
import java.util.Map;

/**
 * The layout for the 2020 main.test.Nautilus ROV.
 * Parses an ROV state and updates the 
 */
public class NautilusLayout implements ROVLayout {

    private static int HORIZONTAL_MOTORS = 4;
    private static final float[] FORWARD_BASE = {1, 1, 1, 1};
    private static final float[] RIGHT_BASE = {1, -1, -1, 1};
    private static final float[] ROTATION_BASE = {1, -1, 1, -1};
    private static final Pin[] HORIZONTAL_MOTOR_PINS = {
            RaspiPin.GPIO_08, // Motor A/0
            RaspiPin.GPIO_09, // Motor B/1
            RaspiPin.GPIO_07, // Motor C/2
            RaspiPin.GPIO_00  // Motor D/3
    };

    private static final Pin[] VERTICAL_MOTOR_PINS = {
            RaspiPin.GPIO_02, // Motor E/4
            RaspiPin.GPIO_03  // Motor F/5
    };

    // Testing
    public static void main(String[] args) throws IOException {
        ServoProvider provider = new RPIServoBlasterProviderCustom();
        ServoDriver driver = provider.getServoDriver(RaspiPin.GPIO_04);
        System.out.println(provider.getDefinedServoPins());
    }

    private float[] horizontalMotorSpeeds;

    /**
     * Computes the horizontal motor speeds for the four horizontal motors based on a state.
     * @param state the state of the motors.
     * @throws IllegalArgumentException if {@code state} == null
     * @return an array of floats ranging from [-1, 1], with the index corresponding to the given motor.
     *      For each motor i, the speed is computed with the following equation:
     *      = (1 - |{@code state.getRotationSpeed()}|) * sqrt(({@code state.getRightSpeed()}^2 * {@code RIGHT_BASE[i]} +
     *      ({@code state.getForwardSpeed()}^2 * {@code FORWARD_BASE[i]}))
     *      + {@code state.getRotationSpeed()} * {@code ROTATION_BASE[i]}
     *
     *      Note that the sqrt operation preserves the sign.
     */
    private static float[] computeHorizontalMotorSpeeds(ROVState state) {
        if(state == null) {
            throw new IllegalArgumentException();
        }

        float rightSquared = (float) Math.pow(state.getRightSpeed(), 2);
        float forwardSquared = (float) Math.pow(state.getForwardSpeed(), 2);

        float[] output = new float[HORIZONTAL_MOTORS];

        // Set the output motor speeds one at a time.
        for(int i = 0; i < HORIZONTAL_MOTORS; i++) {

            // Account for negative forward speed: if negative, negate the direction of movement.
            float forwardBase = FORWARD_BASE[i];
            if (state.getForwardSpeed() < 0) {
                forwardBase = -forwardBase;
            }
            // Do the same for right speed.
            float rightBase = RIGHT_BASE[i];
            if (state.getRightSpeed() < 0) {
                rightBase = - rightBase;
            }

            // Pythagorean Theorem:
            float squaredResult = rightSquared * rightBase + forwardSquared * forwardBase;

            // Total magnitude is the square root of the above result, but we preserve
            // positive/negative signs so that the direction is still correct.
            float horizontalComponent;
            if (squaredResult < 0) {
                horizontalComponent = (float) -(Math.sqrt(-squaredResult)); // Square root, but preserve the sign
            } else {
                horizontalComponent = (float) Math.sqrt(squaredResult); // Square root
            }

            // We scale the horizontal movement as the inverse of the rotation speed.
            // The higher the rotation speed, the smaller the horizontal movement will be.
            float horizontalFinal = (1f - Math.abs(state.getRotationSpeed())) * horizontalComponent;

            // Rotation directions scaled by rotation speed
            float rotationFinal = state.getRotationSpeed() * ROTATION_BASE[i];

            output[i] = horizontalFinal + rotationFinal;
        }
        return output;
    }

    /**
     * Translates a float speed into a ESC-readable value.
     * @param speed the speed, from -1 to 1.
     * @spec.requires -1 <= {@code speed} <= 1
     * @return a mapping of the speed to an integer from 0 to 256.
     */
    private static int translateToESC(float speed) {
        if (speed < -1) {
            speed = -1;
        } else if (speed > 1) {
            speed = 1;
        }

        return (int) (speed + 1) * 128;
    }

    /**
     * Updates the ROVs motors, sensors, and lights to reflect a new ROV state.
     * @param state the new state for the ROV to update to
     * @modifies this
     * @effects updates connected motors of the ROV.
     */
    @Override
    public void update(ROVState state) {
        horizontalMotorSpeeds = computeHorizontalMotorSpeeds(state); // this is a float[]


    }

    /**
     * Returns the speed of the ROVs motors.
     * @return a float array of the ROVs motor speeds, where 1 is full forward and -1 is full backwards.
     */
    @Override
    public float[] getMotorSpeeds() {
        return horizontalMotorSpeeds;
    }

    @Override
    public Map<String, String> getSensors() {
        throw new RuntimeException("Not yet implemented.");
    }
}
