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
        SET_HORIZONTAL_MOVEMENT
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
