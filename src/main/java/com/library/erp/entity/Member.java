package com.library.erp.entity;

import com.library.erp.entity.enums.MembershipStatus;
import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "members", indexes = {
        @Index(name = "idx_member_code", columnList = "member_code")
})
public class Member extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    private User user;

    @Column(name = "member_code", nullable = false, unique = true, length = 40)
    private String memberCode;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "membership_type_id", nullable = false)
    private MembershipType membershipType;

    @Column(name = "address", length = 255)
    private String address;

    @Column(name = "date_of_birth")
    private LocalDate dateOfBirth;

    @Column(name = "occupation", length = 60)
    private String occupation;

    @Column(name = "identity_proof_type", length = 50)
    private String identityProofType;

    @Column(name = "identity_proof_number", length = 80)
    private String identityProofNumber;

    @OneToMany(mappedBy = "member", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List<Membership> memberships = new ArrayList<>();

    public Optional<Membership> getActiveMembership() {
        if (memberships == null) return Optional.empty();
        return memberships.stream()
                .filter(m -> m.getStatus() == MembershipStatus.ACTIVE && m.getExpiryDate().isAfter(LocalDate.now()))
                .findFirst();
    }

    public boolean hasActiveMembership() {
        return getActiveMembership().isPresent() && user.isActive();
    }

    public int getEffectiveBorrowingLimit() {
        return membershipType != null ? membershipType.getBorrowingLimit() : 3;
    }
}
