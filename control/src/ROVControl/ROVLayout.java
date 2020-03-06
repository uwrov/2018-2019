package ROVControl;

import java.util.Map;

public interface ROVLayout {

    /**
     * Updates the ROVs motors, sensors, and lights to reflect a new ROV state.
     * @param state the new state for the ROV to update to
     */
    void update(ROVState state);

    /**
     * Returns the speed of the ROVs motors.
     * @return a float array of the ROVs motor speeds, where 1 is full forward and -1 is full backwards.
     */
    float[] getMotorSpeeds(); // NOTE: THIS SHOULD BE A READONLY COPY!

    /**
     *
     * @return
     */
    Map<String, String> getSensors();
}
