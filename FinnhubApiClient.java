import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import org.json.JSONObject;

public class FinnhubApiClient {

    public static void main(String[] args) {
        // 1. Get your free API key from finnhub.io
        String apiKey = "YOUR_API_KEY"; // Replace with your actual API key
        String stockSymbol = "AAPL";

        // Create a new HttpClient with default settings
        HttpClient client = HttpClient.newHttpClient();

        // Create an HttpRequest
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://finnhub.io/api/v1/quote?symbol=" + stockSymbol + "&token=" + apiKey))
                .build();

        try {
            // 2. Send the request and get the response
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            // Check if the request was successful
            if (response.statusCode() == 200) {
                // 3. Parse the JSON response string
                JSONObject data = new JSONObject(response.body());

                // 4. Print the relevant data
                System.out.println("Stock Quote for " + stockSymbol + ":");
                System.out.println("  Current Price: $" + data.getDouble("c"));
                System.out.println("  Previous Close: $" + data.getDouble("pc"));
                System.out.println("  High of the day: $" + data.getDouble("h"));
                System.out.println("  Low of the day: $" + data.getDouble("l"));
            } else {
                System.out.println("Error: Received response code " + response.statusCode());
            }

        } catch (IOException | InterruptedException e) {
            System.out.println("An error occurred during the API call.");
            e.printStackTrace();
        }
    }
}