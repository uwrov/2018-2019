package Nautilus;
import ROVControl.ROVLayout;
import ROVControl.ROVState;

import java.util.Map;

/**
 * The layout for the 2020 main.test.Nautilus ROV.
 * Parses an ROV state and updates the 
 */
public class NautilusLayout implements ROVLayout {


    @Override
    public void update(ROVState state) {
        throw new RuntimeException("Not yet implemented.");
    }

    @Override
    public Map<String, String> getSensors() {
        throw new RuntimeException("Not yet implemented.");
    }
}
