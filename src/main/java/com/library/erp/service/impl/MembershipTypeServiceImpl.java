package com.library.erp.service.impl;

import com.library.erp.dto.member.MembershipTypeDto;
import com.library.erp.entity.MembershipType;
import com.library.erp.exception.DuplicateResourceException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.MembershipTypeRepository;
import com.library.erp.service.MembershipTypeService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class MembershipTypeServiceImpl implements MembershipTypeService {

    private final MembershipTypeRepository membershipTypeRepository;

    @Override
    public MembershipType createMembershipType(MembershipTypeDto dto) {
        if (membershipTypeRepository.existsByName(dto.getName().trim())) {
            throw new DuplicateResourceException("Membership type '" + dto.getName() + "' already exists.");
        }

        MembershipType type = MembershipType.builder()
                .name(dto.getName().trim())
                .borrowingLimit(dto.getBorrowingLimit())
                .borrowDurationDays(dto.getBorrowDurationDays())
                .gracePeriodDays(dto.getGracePeriodDays() != null ? dto.getGracePeriodDays() : 0)
                .maxRenewals(dto.getMaxRenewals() != null ? dto.getMaxRenewals() : 1)
                .finePerDay(dto.getFinePerDay() != null ? dto.getFinePerDay() : BigDecimal.valueOf(10.00))
                .annualFee(dto.getAnnualFee() != null ? dto.getAnnualFee() : BigDecimal.ZERO)
                .description(dto.getDescription())
                .build();

        return membershipTypeRepository.save(type);
    }

    @Override
    public MembershipType updateMembershipType(Long id, MembershipTypeDto dto) {
        MembershipType type = membershipTypeRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Membership type not found with id: " + id));

        type.setName(dto.getName().trim());
        type.setBorrowingLimit(dto.getBorrowingLimit());
        type.setBorrowDurationDays(dto.getBorrowDurationDays());
        type.setGracePeriodDays(dto.getGracePeriodDays());
        type.setMaxRenewals(dto.getMaxRenewals());
        type.setFinePerDay(dto.getFinePerDay());
        type.setAnnualFee(dto.getAnnualFee());
        type.setDescription(dto.getDescription());

        return membershipTypeRepository.save(type);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<MembershipType> findById(Long id) {
        return membershipTypeRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<MembershipType> findByName(String name) {
        return membershipTypeRepository.findByName(name);
    }

    @Override
    @Transactional(readOnly = true)
    public List<MembershipType> findAllMembershipTypes() {
        return membershipTypeRepository.findAll();
    }

    @Override
    public void seedDefaultMembershipTypesIfEmpty() {
        if (membershipTypeRepository.count() == 0) {
            log.info("Seeding default Membership Types (Student, Faculty, Staff, General)...");
            membershipTypeRepository.save(MembershipType.builder()
                    .name("Student")
                    .borrowingLimit(3)
                    .borrowDurationDays(14)
                    .gracePeriodDays(1)
                    .maxRenewals(2)
                    .finePerDay(BigDecimal.valueOf(10.00))
                    .annualFee(BigDecimal.valueOf(100.00))
                    .description("Standard enrolled university student tier")
                    .build());

            membershipTypeRepository.save(MembershipType.builder()
                    .name("Faculty")
                    .borrowingLimit(10)
                    .borrowDurationDays(30)
                    .gracePeriodDays(3)
                    .maxRenewals(3)
                    .finePerDay(BigDecimal.valueOf(5.00))
                    .annualFee(BigDecimal.ZERO)
                    .description("Professors, teaching faculty and academic researchers")
                    .build());

            membershipTypeRepository.save(MembershipType.builder()
                    .name("Staff")
                    .borrowingLimit(5)
                    .borrowDurationDays(21)
                    .gracePeriodDays(2)
                    .maxRenewals(2)
                    .finePerDay(BigDecimal.valueOf(8.00))
                    .annualFee(BigDecimal.valueOf(50.00))
                    .description("Administrative and technical staff members")
                    .build());

            membershipTypeRepository.save(MembershipType.builder()
                    .name("General")
                    .borrowingLimit(2)
                    .borrowDurationDays(14)
                    .gracePeriodDays(0)
                    .maxRenewals(1)
                    .finePerDay(BigDecimal.valueOf(15.00))
                    .annualFee(BigDecimal.valueOf(250.00))
                    .description("Community and public library patrons")
                    .build());
        }
    }
}
