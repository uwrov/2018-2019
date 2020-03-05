package ROVControl;

import jdk.nashorn.internal.parser.JSONParser;
import org.json.JSONArray;

import java.util.*;
import java.net.URL;
import java.net.HttpURLConnection;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.Reader;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.io.IOException;

public class ROVServer {
   public final String IP_PORT;

   public ROVServer(String ip) {
      IP_PORT = ip;
   }

   // returns a http get response from the server with this subdirectory
   public String getRequest(String subDir, String[] params) throws IOException {
      if (params.length % 2 == 1) {
         throw new IllegalArgumentException("Parameters do not have param/value pairs");
      }

      String parameters = "?";
      for (int i = 0; i < params.length; i += 2) {
         parameters += params[i] + "=" + params[i + 1] + "&";
      }
      parameters = parameters.substring(0, parameters.length() - 1);

      URL serverURL = new URL("http://" + IP_PORT + subDir + parameters);
      HttpURLConnection connection = (HttpURLConnection) serverURL.openConnection();
      connection.setRequestMethod("GET");

      connection.setConnectTimeout(1000);
      connection.setReadTimeout(1000);

      // Reading the response
      int status = connection.getResponseCode();

      Reader streamReader = null;
      if (status > 299) {
         System.err.println("connection error!");
         streamReader = new InputStreamReader(connection.getErrorStream());
      } else {
         streamReader = new InputStreamReader(connection.getInputStream());
      }

      BufferedReader in = new BufferedReader(streamReader);
      String inputLine;
      StringBuffer content = new StringBuffer();
      while ((inputLine = in.readLine()) != null) {
         content.append(inputLine);
      }
      in.close();

      connection.disconnect();

      return content.toString();
   }

   public String getRequest(String subDir) throws IOException{
      return getRequest(subDir, new String[0]);
   }

/**
   public boolean postRequest(String subDir) {
      // posts http request
      URL serverURL = new URL("http://" + IP_PORT + subDir);
      HttpURLConnection connection = (HttpURLConnection) serverURL.openConnection();
      connection.setRequestMethod("POST");
   }
*/
   public JSONArray getCommands() throws IOException {
      JSONParser jsonParser = new JSONParser();
      Object obj = jsonParser.parse(getRequest("/commands"));
      JSONArray list = (JSONArray) obj;
      return list;
   }

}
