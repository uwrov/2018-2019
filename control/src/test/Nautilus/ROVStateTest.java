package test.Nautilus;

import ROVControl.ROVState;
import org.junit.Test;

import static org.junit.Assert.*;

public class ROVStateTest {

    private static float DELTA = 0.000001f;
    private static boolean[] TEST_LIGHTS_STATE = {true, false, true, false, false, true, true};

    // Test setHorizontalSpeed()

    @Test
    public void testSetHorizontalSpeedStoresValues() {
        ROVState state = new ROVState();
        assertEquals(state.getForwardSpeed(), 0f, DELTA);
        assertEquals(state.getRightSpeed(), 0f, DELTA);

        // test setting both to positive
        state.setHorizontalSpeed(0.5f, 1);
        assertEquals(state.getForwardSpeed(), 0.5f, DELTA);
        assertEquals(state.getRightSpeed(), 1, DELTA);

        // test setting to negative
        state.setHorizontalSpeed(-1, -0.1f);
        assertEquals(state.getForwardSpeed(), -1, DELTA);
        assertEquals(state.getRightSpeed(), -0.1f, DELTA);

        // test setting to zero
        state.setHorizontalSpeed(0, 0);
        assertEquals(state.getForwardSpeed(), 0, DELTA);
        assertEquals(state.getRightSpeed(),  0, DELTA);
    }

    @Test (expected = IllegalArgumentException.class)
    public void testSetHorizontalSpeedForwardSpeedTooLarge() {
        ROVState state = new ROVState();
        state.setHorizontalSpeed(2f, 0);
    }

    @Test
    public void testSetVerticalSpeedStoresValues() {
        ROVState state = new ROVState();
        assertEquals(state.getVerticalSpeed(), 0f, DELTA);

        // test setting to positive
        state.setVerticalSpeed(1);
        assertEquals(state.getVerticalSpeed(), 1, DELTA);

        // test setting to negative
        state.setVerticalSpeed(-0.5f);
        assertEquals(state.getVerticalSpeed(), -0.5f, DELTA);

        // test setting to 0
        state.setVerticalSpeed(0);
        assertEquals(state.getVerticalSpeed(), 0, DELTA);
    }

    @Test (expected = IllegalArgumentException.class)
    public void testSetVerticalSpeedTooSmall() {
        ROVState state = new ROVState();
        state.setVerticalSpeed(-2f);
    }

    @Test
    public void testSetRotationalSpeedStoresValues() {
        ROVState state = new ROVState();
        assertEquals(state.getRotationSpeed(), 0f, DELTA);

        //test setting to positive
        state.setRotationSpeed(1);
        assertEquals(state.getRotationSpeed(), 1, DELTA);

        // test setting to negative
        state.setRotationSpeed(-0.5f);
        assertEquals(state.getRotationSpeed(), -0.5f, DELTA);

        // test setting to 0
        state.setRotationSpeed(0);
        assertEquals(state.getRotationSpeed(), 0, DELTA);
    }

    @Test (expected = IllegalArgumentException.class)
    public void testSetRotationSpeedTooSmall() {
        ROVState state = new ROVState();
        state.setRotationSpeed(-2f);
    }

    //////////////////// Lights

    private ROVState makeStateWithLights(boolean[] lights) {
        ROVState state = new ROVState();
        state.setLightsSize(lights.length);

        for (int i = 0; i < lights.length; i++) {
            state.setLightState(i, lights[i]);
        }
        return state;
    }

    /** Test that the initial size of the lights is 0, and that the number of lights can be increased. */
    @Test
    public void testSetLightsSize() {
        ROVState state = new ROVState();
        int size = 10;

        // Should be initialized to 0
        assertEquals(state.getLightsSize(), 0);

        state.setLightsSize(size);
        assertEquals(state.getLightsSize(), size);
    }

    /** Test that added lights are all off. */
    @Test
    public void testSetLightsSizeIsAllOff() {
        ROVState state = new ROVState();
        state.setLightsSize(10);
        for(int i = 0; i < 10; i++) {
            assertFalse(state.getLightState(i));
        }
    }

    /** Test that adding lights does not change existing states. */
    @Test
    public void testSetLightsSizeKeepsOldStates() {
        int finalSize = TEST_LIGHTS_STATE.length + 5;
        ROVState state = makeStateWithLights(TEST_LIGHTS_STATE);

        state.setLightsSize(finalSize); // resize

        for (int i = 0; i < finalSize; i++) {
            if (i < TEST_LIGHTS_STATE.length) {
                assertEquals(state.getLightState(i), TEST_LIGHTS_STATE[i]);
            } else {
                assertFalse(state.getLightState(i));
            }
        }
    }

    @Test
    public void testTurnOnLights() {
        ROVState state = makeStateWithLights(TEST_LIGHTS_STATE);

        state.turnOnLights();
        for (int i = 0; i < state.getLightsSize(); i++) {
            assertTrue(state.getLightState(i));
        }
    }

    @Test
    public void testTurnOffLights() {
        ROVState state = makeStateWithLights(TEST_LIGHTS_STATE);

        state.turnOffLights();
        for (int i = 0; i < state.getLightsSize(); i++) {
            assertFalse(state.getLightState(i));
        }
    }

}
