package test.Nautilus;

import ROVControl.ROVState;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

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

}
