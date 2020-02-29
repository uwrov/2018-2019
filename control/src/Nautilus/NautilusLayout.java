package Nautilus;
import ROVControl.Layout;
import ROVControl.ROVState;

import java.util.Map;

/**
 * The layout for the 2020 main.test.Nautilus ROV.
 * Parses an ROV state and updates the 
 */
public class NautilusLayout implements Layout {


    @Override
    public void update(ROVState state) {
        throw new IllegalArgumentException("Not yet implemented.");
    }

    @Override
    public Map<String, String> getSensors() {
        throw new IllegalArgumentException("Not yet implemented.");
    }
}
