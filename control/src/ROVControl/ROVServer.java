package ROVControl;

import java.util.*;

public class ROVServer {
   public final String IP_PORT;

   public ROVServer(String ip) {
      IP_PORT = ip;
   }

   // returns a http get response from the server with this subdirectory
   public String getRequest(String subDir) {
      URL serverURL = new URL("http://" + IP_PORT + subDir);
      HttpURLConnection connection = (HttpURLConnection) serverURL.openConnection();
      connection.setRequestMethod("GET");

      Map<String, String> parameters = new HashMap<>();
      parameters.put("param1", "val");

      con.setDoOutput(true);
      DataOutputStream out = new DataOutputStream(con.getOutputStream());
      out.writeBytes(ParameterStringBuilder.getParamsString(parameters));
      out.flush();
      out.close();
   }

/**
   public boolean postRequest(String subDir) {
      // posts http request
      URL serverURL = new URL("http://" + IP_PORT + subDir);
      HttpURLConnection connection = (HttpURLConnection) serverURL.openConnection();
      connection.setRequestMethod("POST");
   }
*/
/*   public ArrayList<JSONObject> getCommands() {
      // getrequest("/commands")
   }
   */

}

public class ParameterStringBuilder {
    public static String getParamsString(Map<String, String> params)
      throws UnsupportedEncodingException{
        StringBuilder result = new StringBuilder();

        for (Map.Entry<String, String> entry : params.entrySet()) {
          result.append(URLEncoder.encode(entry.getKey(), "UTF-8"));
          result.append("=");
          result.append(URLEncoder.encode(entry.getValue(), "UTF-8"));
          result.append("&");
        }

        String resultString = result.toString();
        return resultString.length() > 0
          ? resultString.substring(0, resultString.length() - 1)
          : resultString;
    }
}
