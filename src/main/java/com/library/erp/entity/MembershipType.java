package com.library.erp.entity;

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
@Table(name = "membership_types")
public class MembershipType extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false, unique = true, length = 60)
    private String name; // Student, Faculty, Staff, General

    @Column(name = "borrowing_limit", nullable = false)
    @Builder.Default
    private Integer borrowingLimit = 3;

    @Column(name = "borrow_duration_days", nullable = false)
    @Builder.Default
    private Integer borrowDurationDays = 14;

    @Column(name = "grace_period_days", nullable = false)
    @Builder.Default
    private Integer gracePeriodDays = 1;

    @Column(name = "max_renewals", nullable = false)
    @Builder.Default
    private Integer maxRenewals = 2;

    @Column(name = "fine_per_day", nullable = false, precision = 10, scale = 2)
    @Builder.Default
    private BigDecimal finePerDay = BigDecimal.valueOf(10.00);

    @Column(name = "annual_fee", precision = 10, scale = 2)
    @Builder.Default
    private BigDecimal annualFee = BigDecimal.ZERO;

    @Column(name = "description", length = 255)
    private String description;

    @OneToMany(mappedBy = "membershipType")
    @Builder.Default
    private List<Member> members = new ArrayList<>();
}
