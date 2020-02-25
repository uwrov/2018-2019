package ROVControl;

import org.json.JSONObject;

/**
 * Runs the ROV Movement and Surface Communication.
 */
public class MainControl {

    public enum COMMANDS {
        SET_VERTICAL_MOVEMENT,
        SET_HORIZONTAL_MOVEMENT
    }


    public static void main (String[] args) {

    }

    /**
     * Changes a provided ROV State based on the commands.
     * @param commands an array of commands to apply, as JSON Objects
     * @param startingState starting ROV state to modify.
     * @return a new, modified ROV state.
     */
    public ROVState parseServerInput(JSONObject[] commands, ROVState startingState) {
        ROVState state = startingState.copy();
        for (JSONObject command : commands) {
            switch (COMMANDS.valueOf(command.getString("name"))) {
                case SET_VERTICAL_MOVEMENT:
                    setVerticalMovement(command, state);
                    break;
                case SET_HORIZONTAL_MOVEMENT:

                default:
            }
        }

        return state;
    }

    // Sets the vertical movement of a ROVState based on a SET_VERTICAL_MOVEMENT command.
    // Requires that the command has an upward speed value.
    private void setVerticalMovement(JSONObject command, ROVState state) {
        if(command.has("upward_speed")) {
            state.setVerticalSpeed(command.getFloat("upward_speed"));
        } else {
            throw new IllegalArgumentException("Command does not have upward_speed");
        }
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
