package com.automoney.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Value;

import java.util.Map;

@Service
@RequiredArgsConstructor
public class ExternalApiService {

    private final RestTemplate restTemplate;

    // Use environment variable or default to localhost
    // In docker-compose, this should be "http://backend-python:8000"
    @Value("${fastapi.url:http://localhost:8000}")
    private String FASTAPI_URL;

    public Map<String, Object> getStockBalance() {
        return restTemplate.getForObject(FASTAPI_URL + "/bot/balance", Map.class);
    }

    public Map<String, Object> getLottoRecommendation() {
        return restTemplate.getForObject(FASTAPI_URL + "/lotto/recommend", Map.class);
    }
}
