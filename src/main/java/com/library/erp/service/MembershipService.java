package com.library.erp.service;

import com.library.erp.entity.Membership;

import java.util.List;
import java.util.Optional;

public interface MembershipService {
    Membership renewMembership(Long memberId, int extensionMonths);
    boolean isMemberEligibleToBorrow(Long memberId);
    void checkAndExpireOverdueMemberships();
    List<Membership> findExpiredMemberships();
    long countExpiredMemberships();
    Optional<Membership> getActiveMembershipForMember(Long memberId);
}
