package com.library.erp.service.impl;

import com.library.erp.dto.member.MemberProfileDto;
import com.library.erp.dto.member.MemberRegistrationDto;
import com.library.erp.entity.*;
import com.library.erp.entity.enums.MembershipStatus;
import com.library.erp.entity.enums.RoleName;
import com.library.erp.entity.enums.UserStatus;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.*;
import com.library.erp.service.MemberService;
import com.library.erp.service.UserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.Year;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class MemberServiceImpl implements MemberService {

    private final MemberRepository memberRepository;
    private final MembershipRepository membershipRepository;
    private final MembershipTypeRepository membershipTypeRepository;
    private final UserRepository userRepository;
    private final UserService userService;

    @Override
    public Member registerMember(MemberRegistrationDto dto) {
        MembershipType type = membershipTypeRepository.findById(dto.getMembershipTypeId())
                .orElseThrow(() -> new ResourceNotFoundException("Membership Tier not found with id: " + dto.getMembershipTypeId()));

        String password = (dto.getPassword() != null && !dto.getPassword().isBlank()) ? dto.getPassword() : "Member@123";

        User user = User.builder()
                .username(dto.getUsername().trim().toLowerCase())
                .email(dto.getEmail().trim().toLowerCase())
                .password(password)
                .firstName(dto.getFirstName().trim())
                .lastName(dto.getLastName().trim())
                .phone(dto.getPhone())
                .build();

        User savedUser = userService.createUser(user, RoleName.ROLE_MEMBER);

        // Generate unique member code: MEM-YYYY-XXXX
        long count = memberRepository.count() + 1;
        String memberCode = String.format("MEM-%d-%04d", Year.now().getValue(), count);

        Member member = Member.builder()
                .user(savedUser)
                .memberCode(memberCode)
                .membershipType(type)
                .address(dto.getAddress())
                .dateOfBirth(dto.getDateOfBirth())
                .occupation(dto.getOccupation())
                .identityProofType(dto.getIdentityProofType())
                .identityProofNumber(dto.getIdentityProofNumber())
                .build();

        Member savedMember = memberRepository.save(member);

        // Provision initial 1-year active membership
        Membership membership = Membership.builder()
                .member(savedMember)
                .membershipType(type)
                .startDate(LocalDate.now())
                .expiryDate(LocalDate.now().plusYears(1))
                .status(MembershipStatus.ACTIVE)
                .build();

        membershipRepository.save(membership);
        savedMember.getMemberships().add(membership);

        log.info("Registered new library member: {} with code {}", savedUser.getFullName(), memberCode);

        return savedMember;
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Member> findById(Long id) {
        return memberRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Member> findByMemberCode(String memberCode) {
        return memberRepository.findByMemberCode(memberCode.trim().toUpperCase());
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Member> findByUserId(Long userId) {
        return memberRepository.findByUserId(userId);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Member> findByUsername(String username) {
        return memberRepository.findByUserUsername(username);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Member> searchMembers(String query, Pageable pageable) {
        if (query == null || query.trim().isEmpty()) {
            return memberRepository.findAll(pageable);
        }
        return memberRepository.searchMembers(query.trim(), pageable);
    }

    @Override
    public Member updateProfile(Long memberId, MemberProfileDto dto) {
        Member member = memberRepository.findById(memberId)
                .orElseThrow(() -> new ResourceNotFoundException("Member not found with id: " + memberId));

        User user = member.getUser();
        user.setFirstName(dto.getFirstName().trim());
        user.setLastName(dto.getLastName().trim());
        user.setPhone(dto.getPhone());
        userRepository.save(user);

        member.setAddress(dto.getAddress());
        member.setDateOfBirth(dto.getDateOfBirth());
        member.setOccupation(dto.getOccupation());

        return memberRepository.save(member);
    }

    @Override
    public Member toggleMemberStatus(Long memberId) {
        Member member = memberRepository.findById(memberId)
                .orElseThrow(() -> new ResourceNotFoundException("Member not found with id: " + memberId));

        User user = member.getUser();
        user.setStatus(user.getStatus() == UserStatus.ACTIVE ? UserStatus.INACTIVE : UserStatus.ACTIVE);
        userRepository.save(user);

        return member;
    }

    @Override
    @Transactional(readOnly = true)
    public long countTotalMembers() {
        return memberRepository.count();
    }

    @Override
    @Transactional(readOnly = true)
    public long countActiveMembers() {
        return memberRepository.countByStatus(UserStatus.ACTIVE);
    }
}
