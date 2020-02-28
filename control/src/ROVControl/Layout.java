package ROVControl;

import java.util.Map;

public interface Layout {

    /**
     * Updates the ROVs motors, sensors, and lights to reflect a new ROV state.
     * @param state the new state for the ROV to update to
     */
    void update(ROVState state);

    /**
     *
     * @return
     */
    Map<String, String> getSensors();
}
