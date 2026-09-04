package com.library.erp.entity;

import com.library.erp.entity.enums.CopyCondition;
import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "return_records")
public class ReturnRecord extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "borrow_record_id", nullable = false, unique = true)
    private BorrowRecord borrowRecord;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "librarian_id")
    private Librarian librarian;

    @Column(name = "return_date", nullable = false)
    private LocalDate returnDate;

    @Column(name = "days_overdue", nullable = false)
    @Builder.Default
    private Integer daysOverdue = 0;

    @Column(name = "fine_assessed", precision = 10, scale = 2)
    @Builder.Default
    private BigDecimal fineAssessed = BigDecimal.ZERO;

    @Enumerated(EnumType.STRING)
    @Column(name = "returned_condition", length = 30)
    @Builder.Default
    private CopyCondition returnedCondition = CopyCondition.GOOD;

    @Column(name = "remarks", length = 255)
    private String remarks;
}
