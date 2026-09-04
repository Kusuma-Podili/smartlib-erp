package com.library.erp.entity;

import com.library.erp.entity.enums.MembershipStatus;
import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "memberships", indexes = {
        @Index(name = "idx_membership_expiry", columnList = "expiry_date"),
        @Index(name = "idx_membership_status", columnList = "status")
})
public class Membership extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "member_id", nullable = false)
    private Member member;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "membership_type_id", nullable = false)
    private MembershipType membershipType;

    @Column(name = "start_date", nullable = false)
    private LocalDate startDate;

    @Column(name = "expiry_date", nullable = false)
    private LocalDate expiryDate;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 30)
    @Builder.Default
    private MembershipStatus status = MembershipStatus.ACTIVE;

    public boolean isExpired() {
        return LocalDate.now().isAfter(expiryDate);
    }
}
