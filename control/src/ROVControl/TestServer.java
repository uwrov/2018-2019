package ROVControl;

import java.io.IOException;

public class TestServer {
   public static void main(String[] args) throws IOException {
      ROVServer server = new ROVServer("localhost:8080");
      System.out.println(server.getRequest("/commands", new String[]{"sup", "hi"}));
   }
}
