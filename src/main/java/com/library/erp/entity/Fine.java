package com.library.erp.entity;

import com.library.erp.entity.enums.FineStatus;
import com.library.erp.entity.enums.FineType;
import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "fines", indexes = {
        @Index(name = "idx_fine_status", columnList = "status"),
        @Index(name = "idx_fine_member", columnList = "member_id")
})
public class Fine extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "borrow_record_id")
    private BorrowRecord borrowRecord;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "member_id", nullable = false)
    private Member member;

    @Enumerated(EnumType.STRING)
    @Column(name = "fine_type", nullable = false, length = 40)
    private FineType fineType;

    @Column(name = "amount", nullable = false, precision = 10, scale = 2)
    private BigDecimal amount;

    @Column(name = "paid_amount", nullable = false, precision = 10, scale = 2)
    @Builder.Default
    private BigDecimal paidAmount = BigDecimal.ZERO;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 30)
    @Builder.Default
    private FineStatus status = FineStatus.UNPAID;

    @Column(name = "reason", length = 255)
    private String reason;

    @OneToMany(mappedBy = "fine", cascade = CascadeType.ALL)
    @Builder.Default
    private List<FinePayment> payments = new ArrayList<>();

    public BigDecimal getOutstandingBalance() {
        return amount.subtract(paidAmount != null ? paidAmount : BigDecimal.ZERO);
    }
}
