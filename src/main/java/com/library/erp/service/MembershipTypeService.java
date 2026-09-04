package com.library.erp.service;

import com.library.erp.dto.member.MembershipTypeDto;
import com.library.erp.entity.MembershipType;

import java.util.List;
import java.util.Optional;

public interface MembershipTypeService {
    MembershipType createMembershipType(MembershipTypeDto dto);
    MembershipType updateMembershipType(Long id, MembershipTypeDto dto);
    Optional<MembershipType> findById(Long id);
    Optional<MembershipType> findByName(String name);
    List<MembershipType> findAllMembershipTypes();
    void seedDefaultMembershipTypesIfEmpty();
}
