package com.library.erp.service;

import com.library.erp.dto.member.MemberProfileDto;
import com.library.erp.dto.member.MemberRegistrationDto;
import com.library.erp.entity.Member;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.Optional;

public interface MemberService {
    Member registerMember(MemberRegistrationDto dto);
    Optional<Member> findById(Long id);
    Optional<Member> findByMemberCode(String memberCode);
    Optional<Member> findByUserId(Long userId);
    Optional<Member> findByUsername(String username);
    Page<Member> searchMembers(String query, Pageable pageable);
    Member updateProfile(Long memberId, MemberProfileDto dto);
    Member toggleMemberStatus(Long memberId);
    long countTotalMembers();
    long countActiveMembers();
}
