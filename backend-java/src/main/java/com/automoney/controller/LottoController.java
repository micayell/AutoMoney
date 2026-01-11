package com.automoney.controller;

import com.automoney.service.ExternalApiService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/api/lotto")
@RequiredArgsConstructor
public class LottoController {

    private final ExternalApiService externalApiService;

    @GetMapping("/recommend")
    public ResponseEntity<Map<String, Object>> getRecommendation() {
        return ResponseEntity.ok(externalApiService.getLottoRecommendation());
    }
}

