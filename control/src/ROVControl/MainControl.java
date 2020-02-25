package ROVControl;

import org.json.JSONObject;

/**
 * Runs the ROV Movement and Surface Communication.
 */
public class MainControl {

    public enum COMMANDS {
        SET_VERTICAL_MOVEMENT
    }


    public static void main (String[] args) {

    }

    /**
     * Changes a provided ROV State based on the commands.
     * @param commands an array of commands to apply, as JSON Objects
     * @param state starting ROV state to modify.
     * @return a new, modified ROV state.
     */
    public ROVState parseServerInput(JSONObject[] commands, ROVState state) {

    }

    /**
     * Retrieves an array of commands from the server.
     * @param address address of the server to retrieve data from
     * @requires address is not null
     * @throws java.io.IOException if server cannot be contacted
     * @return an array of commands, represented by JSON Objects.
     */
    public JSONObject[] getInputFromServer(String address) {
        return null;
    }

}
