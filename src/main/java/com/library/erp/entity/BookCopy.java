package com.library.erp.entity;

import com.library.erp.entity.enums.CopyCondition;
import com.library.erp.entity.enums.CopyStatus;
import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "book_copies", indexes = {
        @Index(name = "idx_copy_barcode", columnList = "barcode"),
        @Index(name = "idx_copy_status", columnList = "availability_status")
})
public class BookCopy extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "book_id", nullable = false)
    private Book book;

    @Column(name = "barcode", nullable = false, unique = true, length = 60)
    private String barcode;

    @Column(name = "copy_number", nullable = false)
    private Integer copyNumber;

    @Enumerated(EnumType.STRING)
    @Column(name = "condition_status", nullable = false, length = 30)
    @Builder.Default
    private CopyCondition conditionStatus = CopyCondition.NEW;

    @Enumerated(EnumType.STRING)
    @Column(name = "availability_status", nullable = false, length = 30)
    @Builder.Default
    private CopyStatus availabilityStatus = CopyStatus.AVAILABLE;

    @Column(name = "acquired_date")
    @Builder.Default
    private LocalDate acquiredDate = LocalDate.now();

    @Column(name = "remarks", length = 255)
    private String remarks;

    public boolean isAvailable() {
        return this.availabilityStatus == CopyStatus.AVAILABLE;
    }
}
