package com.automoney.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@Table(name = "assets")
@Getter @Setter
public class Asset {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private AssetType type; // CASH, STOCK, REAL_ESTATE, SAVING

    @Column(nullable = false)
    private BigDecimal amount;

    private String description;

    private LocalDate date;

    public enum AssetType {
        CASH, STOCK, REAL_ESTATE, SAVING, DEBT
    }
}

