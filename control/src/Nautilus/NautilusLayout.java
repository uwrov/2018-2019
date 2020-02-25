package Nautilus;
import ROVControl.ROVState;
import jdk.jshell.spi.ExecutionControl;

import java.util.Map;

/**
 * The layout for the 2020 Nautilus ROV.
 * Parses an ROV state and updates the 
 */
public class NautilusLayout implements ROVControl.Layout {


    @Override
    public void update(ROVState state) {
        throw new IllegalArgumentException("Not yet implemented.");
    }

    @Override
    public Map<String, String> getSensors() {
        throw new IllegalArgumentException("Not yet implemented.");
    }
}
