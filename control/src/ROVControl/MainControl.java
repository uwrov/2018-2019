package ROVControl;

import Nautilus.NautilusLayout;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;

/**
 * Runs the ROV Movement and Surface Communication.
 */
public class MainControl {

    public enum COMMANDS {
        SET_VERTICAL_MOVEMENT,
        SET_HORIZONTAL_MOVEMENT,
        SET_FORWARD_MOVEMENT,
        SET_RIGHT_MOVEMENT,
        SET_ROTATION_MOVEMENT,
        TURN_ON_LIGHTS,
        TURN_OFF_LIGHTS,
        SET_LIGHT_STATE,
    }

    private static String SERVER_URL = "";
    private static int SERVER_TIMEOUT = 2000;

    public static void main (String[] args) throws IOException {
        ROVState state = new ROVState();
        ROVLayout layout = new NautilusLayout();

        layout.update(state);

        while (true) {
            URL serverURL =  new URL(SERVER_URL);

            JSONArray commands = getInputFromServer(serverURL);
        }
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
                    setHorizontalMovement(command, state);
                    break;
                case SET_FORWARD_MOVEMENT:
                    setForwardMovement(command, state);
                    break;
                case SET_RIGHT_MOVEMENT:
                    setRightMovement(command, state);
                    break;
                case SET_ROTATION_MOVEMENT:
                    setRotationMovement(command, state);
                    break;
                case TURN_ON_LIGHTS:
                    setLightsOn(state);
                    break;
                case TURN_OFF_LIGHTS:
                    setLightsOff(state);
                    break;
                case SET_LIGHT_STATE:
                    changeLightState(command, state);
                    break;
                default:
            }
        }

        return state;
    }

    /**
     * Sets the vertical movement of a ROVState based on a SET_VERTICAL_MOVEMENT command.
     * @param command the Vertical Movement command
     * @param state ROVState to modify
     * @requires {@code state} != null, {@code command} != null, {@code command} has parameter {@code upward_speed}
     * @modifies state
     *
     */
    private void setVerticalMovement(JSONObject command, ROVState state) {
        if(command.has("upward_speed")) {
            state.setVerticalSpeed(command.getFloat("upward_speed"));
        } else {
            throw new IllegalArgumentException("Command does not have upward_speed.");
        }
    }

    /**
     * Sets the horizontal movement of a ROVState based on a SET_HORIZONTAL_MOVEMENT command.
     * @param command the Horizontal Movement command
     * @param state ROVState to modify
     * @requires {@code state} != null, {@code command} != null, {@code command} has parameter {@code forward_speed}
     *           and {@code right_speed}
     * @modifies state
     */
    private void setHorizontalMovement(JSONObject command, ROVState state) {
        if (!command.has("forward_speed")) {
            throw new IllegalArgumentException("Command does not have forward_speed.");
        }
        if (!command.has("right_speed")) {
            throw new IllegalArgumentException("Command does not have right_speed.");
        }
        setForwardMovement(command, state);
        setRightMovement(command, state);
    }

    /**
     * Sets the forward movement of a ROVState base on a SET_FORWARD_MOVEMENT command.
     * @param command the Forward Movement command
     * @param state ROVState to modify
     * @requires {@code state} != null, {@code command} != null, {@code command} has parameter {@code forward_speed}
     * @modifies state
     */
    private void setForwardMovement(JSONObject command, ROVState state) {
        if(command.has("forward_speed")) {
            state.setForwardSpeed(command.getFloat("forward_speed"));
        } else {
            throw new IllegalArgumentException("Command does not have forward_speed.");
        }
    }

    /**
     * Sets the right movement of a ROVState base on a SET_RIGHT_MOVEMENT command.
     * @param command the Right Movement command
     * @param state ROVState to modify
     * @requires {@code state} != null, {@code command} != null, {@code command} has parameter {@code right_speed}
     * @modifies state
     */
    private void setRightMovement(JSONObject command, ROVState state) {
        if(command.has("right_speed")) {
            state.setRightSpeed(command.getFloat("right_speed"));
        } else {
            throw new IllegalArgumentException("Command does not have right_speed.");
        }
    }

    /**
     * Sets the rotational movement of a ROVState base on a SET_ROTATION_MOVEMENT command.
     * @param command the Rotation Movement command
     * @param state ROVState to modify
     * @requires {@code state} != null, {@code command} != null, {@code command} has parameter {@code rotate_speed}
     * @modifies state
     */
    private void setRotationMovement(JSONObject command, ROVState state) {
        if(command.has("rotate_speed")) {
            state.setRotationSpeed(command.getFloat("rotate_speed"));
        } else {
            throw new IllegalArgumentException("Command does not have rotate_speed.");
        }
    }

    /**
     * Changes the states of all the lights in ROVState to on base on a TURN_ON_LIGHTS command.
     * @param state ROVState to modify
     * @modifies state
     */
    private void setLightsOn(ROVState state) {
        state.turnOnLights();
    }

    /**
     * Changes the states of all the lights in ROVState to off base on a TURN_OFF_LIGHTS command.
     * @param state ROVState to modify
     * @modifies state
     */
    private void setLightsOff(ROVState state) {
        state.turnOffLights();
    }

    /**
     * Sets the light state of a specific light in ROVState base on a SET_LIGHT_STATE command.
     * @param command the Set Light State command
     * @param state ROVState to modify
     * @requires {@code state} != null, {@code command} != null, {@code command} has parameter {@code id} and has
     *           {@code state}
     * @modifies state
     */
    private void changeLightState(JSONObject command, ROVState state) {
        if (!command.has("id")) {
            throw new IllegalArgumentException("Command does not have id.");
        }
        if (!command.has("state")) {
            throw new IllegalArgumentException("Command does not have state.");
        }
        state.setLightState(command.getInt("id"), command.getBoolean("state"));
    }

    /**
     * Retrieves an array of commands from the server.
     * @param url URL address of the server to retrieve data from
     * @requires {@code url} is not null
     * @throws java.io.IOException if server cannot be contacted
     * @return an array of commands, represented by JSON Objects.
     */
    public static JSONArray getInputFromServer(URL url) throws IOException {
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        //connection.setRequestProperty("");
        connection.setConnectTimeout(SERVER_TIMEOUT);
        connection.setReadTimeout(SERVER_TIMEOUT);
        BufferedReader input = new BufferedReader(
                new InputStreamReader(connection.getInputStream()));

        // Delete after implementing
        throw new RuntimeException("Not yet implemented");
    }

}
