package test.Nautilus;

import ROVControl.ROVState;
import java.util.*;
import org.junit.Test;

import static org.junit.Assert.*;

public class ROVStateTest {

    private static float DELTA = 0.000001f;

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

    @Test
    public void testTurnOnLights() {
        ROVState state = new ROVState();
        state.turnOnLights();
        for (int i = 0; i < state.getLightsSize(); i++) {
            assertTrue(state.getLightState(i));
        }
    }

    @Test
    public void testTurnOffLights() {
        ROVState state = new ROVState();
        state.turnOffLights();
        for (int i = 0; i < state.getLightsSize(); i++) {
            assertFalse(state.getLightState(i));
        }
    }

}
