package Nautilus;
import ROVControl.ROVLayout;
import ROVControl.ROVState;

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
    private float[] computeHorizontalMotorSpeeds(ROVState state) {
        if(state == null) {
            throw new IllegalArgumentException();
        }

        float rightSquared = (float) Math.pow(state.getRightSpeed(), 2);
        float forwardSquared = (float) Math.pow(state.getForwardSpeed(), 2);

        float[] output = new float[HORIZONTAL_MOTORS];

        // Set the output values
        for(int i = 0; i < HORIZONTAL_MOTORS; i++) {
            // Account for negative directions
            float forwardBase = FORWARD_BASE[i];
            if (state.getForwardSpeed() < 0) {
                forwardBase = -forwardBase;
            }
            float rightBase = RIGHT_BASE[i];
            if (state.getRightSpeed() < 0) {
                rightBase = - rightBase;
            }

            // Pythagorean Theorem:
            float squaredResult = rightSquared * rightBase + forwardSquared * forwardBase;

            float horizontalComponent;
            if (squaredResult < 0) {
                horizontalComponent = (float) -(Math.sqrt(-squaredResult)); // Square root, but preserve the sign
            } else {
                horizontalComponent = (float) Math.sqrt(squaredResult); // Square root
            }

            // (1 - |rotationSpeed|)
            float horizontalComponentScalar = (1f - Math.abs(state.getRotationSpeed()));

            output[i] = horizontalComponentScalar * horizontalComponent + state.getRotationSpeed() * ROTATION_BASE[i];
        }
        return output;
    }

    @Override
    public void update(ROVState state) {

        float[] horizontalMotorSpeeds = computeHorizontalMotorSpeeds(state);

        throw new RuntimeException("Not yet implemented.");


    }

    @Override
    public Map<String, String> getSensors() {
        throw new RuntimeException("Not yet implemented.");
    }
}
