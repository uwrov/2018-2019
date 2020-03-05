package ROVControl;

public class TestServer {
   public static void main(String[] args) {
      ROVServer server = new ROVServer("localhost:8080");
      System.out.println(server.getRequest("/commands"));
   }
}
