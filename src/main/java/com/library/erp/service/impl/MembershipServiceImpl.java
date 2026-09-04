package com.library.erp.service.impl;

import com.library.erp.entity.Member;
import com.library.erp.entity.Membership;
import com.library.erp.entity.enums.MembershipStatus;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.MemberRepository;
import com.library.erp.repository.MembershipRepository;
import com.library.erp.service.MembershipService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class MembershipServiceImpl implements MembershipService {

    private final MembershipRepository membershipRepository;
    private final MemberRepository memberRepository;

    @Override
    public Membership renewMembership(Long memberId, int extensionMonths) {
        Member member = memberRepository.findById(memberId)
                .orElseThrow(() -> new ResourceNotFoundException("Member not found with id: " + memberId));

        Optional<Membership> activeOpt = membershipRepository
                .findFirstByMemberIdAndStatusOrderByExpiryDateDesc(memberId, MembershipStatus.ACTIVE);

        LocalDate newStartDate = LocalDate.now();
        LocalDate newExpiryDate;

        if (activeOpt.isPresent()) {
            Membership current = activeOpt.get();
            LocalDate baseDate = current.getExpiryDate().isAfter(LocalDate.now()) ? current.getExpiryDate() : LocalDate.now();
            newExpiryDate = baseDate.plusMonths(extensionMonths);
            current.setExpiryDate(newExpiryDate);
            return membershipRepository.save(current);
        } else {
            newExpiryDate = newStartDate.plusMonths(extensionMonths);
            Membership newMembership = Membership.builder()
                    .member(member)
                    .membershipType(member.getMembershipType())
                    .startDate(newStartDate)
                    .expiryDate(newExpiryDate)
                    .status(MembershipStatus.ACTIVE)
                    .build();
            return membershipRepository.save(newMembership);
        }
    }

    @Override
    @Transactional(readOnly = true)
    public boolean isMemberEligibleToBorrow(Long memberId) {
        Member member = memberRepository.findById(memberId)
                .orElseThrow(() -> new ResourceNotFoundException("Member not found with id: " + memberId));

        if (!member.getUser().isActive()) {
            log.warn("Member {} user account is not active.", member.getMemberCode());
            return false;
        }

        Optional<Membership> activeMembership = getActiveMembershipForMember(memberId);
        if (activeMembership.isEmpty()) {
            log.warn("Member {} does not hold an active membership.", member.getMemberCode());
            return false;
        }

        if (activeMembership.get().isExpired()) {
            log.warn("Member {} membership expired on {}.", member.getMemberCode(), activeMembership.get().getExpiryDate());
            return false;
        }

        return true;
    }

    /**
     * Nightly cron job to scan and flag expired memberships.
     */
    @Override
    @Scheduled(cron = "0 0 1 * * ?") // 1:00 AM daily
    public void checkAndExpireOverdueMemberships() {
        log.info("Running scheduled membership expiration audit...");
        List<Membership> expired = membershipRepository.findExpiredMemberships(LocalDate.now());
        for (Membership m : expired) {
            m.setStatus(MembershipStatus.EXPIRED);
        }
        membershipRepository.saveAll(expired);
        log.info("Membership expiration audit processed {} expired records.", expired.size());
    }

    @Override
    @Transactional(readOnly = true)
    public List<Membership> findExpiredMemberships() {
        return membershipRepository.findExpiredMemberships(LocalDate.now());
    }

    @Override
    @Transactional(readOnly = true)
    public long countExpiredMemberships() {
        return membershipRepository.countByStatus(MembershipStatus.EXPIRED);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Membership> getActiveMembershipForMember(Long memberId) {
        return membershipRepository.findFirstByMemberIdAndStatusOrderByExpiryDateDesc(memberId, MembershipStatus.ACTIVE);
    }
}
