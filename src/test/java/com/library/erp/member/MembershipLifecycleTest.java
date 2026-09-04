package com.library.erp.member;

import com.library.erp.dto.member.MemberRegistrationDto;
import com.library.erp.dto.member.MembershipTypeDto;
import com.library.erp.entity.Member;
import com.library.erp.entity.Membership;
import com.library.erp.entity.MembershipType;
import com.library.erp.entity.enums.MembershipStatus;
import com.library.erp.entity.enums.UserStatus;
import com.library.erp.repository.MembershipRepository;
import com.library.erp.repository.UserRepository;
import com.library.erp.service.MemberService;
import com.library.erp.service.MembershipService;
import com.library.erp.service.MembershipTypeService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class MembershipLifecycleTest {

    @Autowired
    private MemberService memberService;

    @Autowired
    private MembershipService membershipService;

    @Autowired
    private MembershipTypeService membershipTypeService;

    @Autowired
    private MembershipRepository membershipRepository;

    @Autowired
    private UserRepository userRepository;

    private MembershipType studentTier;
    private MembershipType facultyTier;

    @BeforeEach
    void setUp() {
        studentTier = membershipTypeService.findByName("Student").orElseGet(() ->
                membershipTypeService.createMembershipType(MembershipTypeDto.builder()
                        .name("Student")
                        .borrowingLimit(3)
                        .borrowDurationDays(14)
                        .gracePeriodDays(1)
                        .finePerDay(BigDecimal.valueOf(10.00))
                        .build())
        );

        facultyTier = membershipTypeService.findByName("Faculty").orElseGet(() ->
                membershipTypeService.createMembershipType(MembershipTypeDto.builder()
                        .name("Faculty")
                        .borrowingLimit(10)
                        .borrowDurationDays(30)
                        .gracePeriodDays(3)
                        .finePerDay(BigDecimal.valueOf(5.00))
                        .build())
        );
    }

    @Test
    @DisplayName("Test 1: Member registration creates member with unique ID and 1-year active subscription")
    void memberRegistrationProvisionsActiveSubscription() {
        String unique = "patron_" + System.currentTimeMillis();
        MemberRegistrationDto dto = MemberRegistrationDto.builder()
                .username(unique)
                .email(unique + "@library.test")
                .firstName("Alice")
                .lastName("Smith")
                .membershipTypeId(studentTier.getId())
                .phone("9876543210")
                .address("Block C, Hall 4")
                .build();

        Member member = memberService.registerMember(dto);

        assertThat(member.getId()).isNotNull();
        assertThat(member.getMemberCode()).startsWith("MEM-");
        assertThat(member.getUser().hasRole("ROLE_MEMBER")).isTrue();
        assertThat(member.hasActiveMembership()).isTrue();
        assertThat(member.getEffectiveBorrowingLimit()).isEqualTo(3);
        assertThat(membershipService.isMemberEligibleToBorrow(member.getId())).isTrue();
    }

    @Test
    @DisplayName("Test 2: Membership renewal extends the expiry date by configured months")
    void membershipRenewalExtendsExpiryDate() {
        String unique = "renew_" + System.currentTimeMillis();
        Member member = memberService.registerMember(MemberRegistrationDto.builder()
                .username(unique)
                .email(unique + "@library.test")
                .firstName("Bob")
                .lastName("Taylor")
                .membershipTypeId(studentTier.getId())
                .build());

        Membership initialMembership = membershipService.getActiveMembershipForMember(member.getId()).orElseThrow();
        LocalDate originalExpiry = initialMembership.getExpiryDate();

        // Renew by 6 months
        Membership renewed = membershipService.renewMembership(member.getId(), 6);

        assertThat(renewed.getExpiryDate()).isEqualTo(originalExpiry.plusMonths(6));
        assertThat(renewed.getStatus()).isEqualTo(MembershipStatus.ACTIVE);
    }

    @Test
    @DisplayName("Test 3: Expired membership prevents borrowing eligibility")
    void expiredMembershipBlocksBorrowing() {
        String unique = "expired_" + System.currentTimeMillis();
        Member member = memberService.registerMember(MemberRegistrationDto.builder()
                .username(unique)
                .email(unique + "@library.test")
                .firstName("Charlie")
                .lastName("Brown")
                .membershipTypeId(studentTier.getId())
                .build());

        Membership ms = membershipService.getActiveMembershipForMember(member.getId()).orElseThrow();
        // Manually backdate expiry to the past
        ms.setExpiryDate(LocalDate.now().minusDays(5));
        membershipRepository.save(ms);

        boolean eligible = membershipService.isMemberEligibleToBorrow(member.getId());
        assertThat(eligible).isFalse();
    }

    @Test
    @DisplayName("Test 4: Inactive patron account prevents borrowing eligibility")
    void inactiveUserAccountBlocksBorrowing() {
        String unique = "inactive_" + System.currentTimeMillis();
        Member member = memberService.registerMember(MemberRegistrationDto.builder()
                .username(unique)
                .email(unique + "@library.test")
                .firstName("David")
                .lastName("Miller")
                .membershipTypeId(facultyTier.getId())
                .build());

        // Deactivate user account
        memberService.toggleMemberStatus(member.getId());
        assertThat(member.getUser().getStatus()).isEqualTo(UserStatus.INACTIVE);

        boolean eligible = membershipService.isMemberEligibleToBorrow(member.getId());
        assertThat(eligible).isFalse();
    }
}
