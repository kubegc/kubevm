package com.github.lightweight;

import okhttp3.*;

import java.io.IOException;
import java.util.logging.Logger;

public class LightweightKubernetesClient {
    private String ip;
    private String prefix;
    private String port;
    private String token;
    private String authType;
    private OkHttpClient client;
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");

    public final static Logger m_logger = Logger.getLogger(LightweightKubernetesClient.class.getName());

    public LightweightKubernetesClient(String prefix,String ip, String port, String token, String authType) {
        this.ip = ip;
        this.prefix = prefix;
        this.port = port;
        this.token = token;
        this.authType = authType;
    }

    public OkHttpClient getClient() {
        return client;
    }

    public void setClient(OkHttpClient client) {
        this.client = client;
    }

    private String handleResponse(Request request){
        try (Response response = client.newCall(request).execute()) {
            m_logger.info(" "+request.url()+":");
            m_logger.info(response.body().string());
            return response.body().string();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public String initHttps(){
        Request request = new Request.Builder()
                .url(this.prefix+"://"+this.ip+":"+this.port)
                .addHeader("Authorization",this.authType+" "+this.token)
                .get()
                .build();
        m_logger.info(request.url().toString());
        m_logger.info(request.header("Authorization"));
        return handleResponse(request);
    }

    public String postHttps(String url, String json){
        RequestBody body = RequestBody.create(JSON, json);
        Request request = new Request.Builder()
                .url(url)
                .addHeader("Authorization","Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0aW5nZmVuZyIsInJvbGVzIjpbIk1FTUJFUiJdLCJpYXQiOjE1MjM0Mzg4ODYsImV4cCI6MTUyMzQ0MjQzMH0.5oQU1HUekYxP6BE534Vek_O6ZXhwPbUXQJuBB_da8r8")
                .post(body)
                .build();
        return handleResponse(request);
    }
}
