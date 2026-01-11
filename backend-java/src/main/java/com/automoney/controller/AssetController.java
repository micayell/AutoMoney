package com.automoney.controller;

import com.automoney.entity.Asset;
import com.automoney.service.AssetService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/assets")
@RequiredArgsConstructor
public class AssetController {

    private final AssetService assetService;

    // TODO: Get user ID from Security Context
    private final Long TEMP_USER_ID = 1L;

    @GetMapping
    public ResponseEntity<List<Asset>> getMyAssets() {
        return ResponseEntity.ok(assetService.getAssetsByUserId(TEMP_USER_ID));
    }

    @PostMapping
    public ResponseEntity<Asset> createAsset(@RequestBody Asset asset) {
        // TODO: Set user based on auth
        return ResponseEntity.ok(assetService.saveAsset(asset));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteAsset(@PathVariable Long id) {
        assetService.deleteAsset(id);
        return ResponseEntity.ok().build();
    }
}

