package com.automoney.service;

import com.automoney.entity.Asset;
import com.automoney.repository.AssetRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class AssetService {

    private final AssetRepository assetRepository;

    public List<Asset> getAssetsByUserId(Long userId) {
        return assetRepository.findByUserId(userId);
    }

    @Transactional
    public Asset saveAsset(Asset asset) {
        return assetRepository.save(asset);
    }

    @Transactional
    public void deleteAsset(Long assetId) {
        assetRepository.deleteById(assetId);
    }
}

