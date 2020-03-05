package test.Nautilus;

import Nautilus.NautilusLayout;
import ROVControl.ROVState;
import org.junit.Test;

import static org.junit.Assert.assertTrue;

public class NautilusLayoutTest {

    private static float DELTA = 0.00001f;


    //////// computeHorizontalMotorSpeeds

    private ROVState buildState(float forwardSpeed, float rightSpeed, float rotationSpeed, float verticalSpeed) {
        ROVState state = new ROVState();
        state.setForwardSpeed(forwardSpeed);
        state.setRightSpeed(rightSpeed);
        state.setRotationSpeed(rotationSpeed);
        state.setVerticalSpeed(verticalSpeed);
        return state;
    }

    private boolean compareFloatArrays(float[] f1, float[] f2) {
        if (f1.length != f2.length) {
            return false;
        } else {
            for (int i = 0; i < f1.length; i++) {
                if (Math.abs(f1[i] - f2[i]) > DELTA) {
                    return false;
                }
            }
            return true;
        }
    }

    @Test
    /** Test result when the rotation speeds are zero*/
    public void testCHMSSpeedIsZero() {
        ROVState state = buildState(0, 0, 0, 0);
        //float[] motorStates = NautilusLayout.computeHorizontalMotorSpeeds(state);

        //assertTrue(compareFloatArrays(motorStates, new float[] {0, 0, 0, 0}));
    }

}
